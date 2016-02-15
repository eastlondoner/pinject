import pinject
from lazy import lazy
import types
import functools
import inspect
import re
import pinject.bindings
from threading import Lock
import tdash as _


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def convert(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

service_loaders = {}

def monkey_patch_instance(self, new_method_name, new_method):
    setattr(self, new_method_name, types.MethodType(new_method, self))

class SomeBindingSpec(pinject.BindingSpec):
    def __init__(self, key, actual_configure=None):
        self.key = key
        self.actual_configure = actual_configure

    def configure(self, bind, require):
        if self.actual_configure:
            self.actual_configure(bind, require)

    def __eq__(self, other):
        return (type(self) == type(other) and self.key == other.key)


fetch_lock = Lock()
def fetch_service_loader(name):
    with fetch_lock:
        sl = service_loaders.get(name, ServiceLoader(name))
    return sl

class ServiceLoader():
    def __init__(self, name):
        if name in service_loaders:
            raise Exception("cannot instantiate multiple service loaders with same name")
        service_loaders[name] = self

        self._object_graph_initialised = False
        self._binding_specs = []
        self._class_mappings = {}
        self._arg_mappings = {}
        self._classes = []

    @lazy
    def object_graph(self):
        """
        :type
        Returns:

        """

        og = pinject.new_object_graph(binding_specs=self._binding_specs, modules=None, classes=self._classes)

        def call_with_injection(self, fn, *direct_pargs, **direct_kwargs):
            return self._obj_provider.call_with_injection(fn, self._injection_context_factory.new(fn), direct_pargs, direct_kwargs)

        def inject_method(self, fn, *args, **kwargs):

            pargs, kwargs = self._obj_provider.get_injection_pargs_kwargs(fn.__init__ if inspect.isclass(fn) else fn, self._injection_context_factory.new(fn), args, kwargs)
            print "pargs", pargs
            print "kwargs", kwargs
            return functools.partial(fn, *pargs, **kwargs)

        ## MONKEY PATCHING HAHAHAHA
        monkey_patch_instance(og, 'call_with_injection', call_with_injection)
        monkey_patch_instance(og, 'inject_method', inject_method)

        self._object_graph_initialised = True
        return og


    def register_implementation(self, implementation_class, base_class=None, with_name=None, singleton=False, args=(), kwargs={}):
        """
        Registers implementation_class as the implementation for implementation class and all its base classes

        :param implementation_class:
        :type implementation_class: class
        :param base_class:
        :type base_class: class
        :param with_name:
        :type with_name: str
        :param singleton:
        :type singleton: bool
        :param args:
        :type args: tuple
        :param kwargs:
        :type kwargs: dict
        :return: None
        """

        if self._object_graph_initialised:
            raise Exception("cannot register further dependencies after initialising Service Loader")

        assert inspect.isclass(implementation_class)
        self._classes.append(implementation_class)
        names = [implementation_class.__name__, with_name] if with_name else [implementation_class.__name__]

        if base_class:
            assert inspect.isclass(base_class)
            assert issubclass(implementation_class, base_class)
            names.append(base_class.__name__)
        else:
            names += [clazz.__name__ for clazz in inspect.getmro(implementation_class) if inspect.isclass(clazz)]

        names = list(set(names) - set(['object']))
        map(lambda name: self._class_mappings.update({name:implementation_class}), names)
        #names = map(convert, names)
        print "Registering {} for :".format(implementation_class), names


        def register(bind, require):
            for name in names:
                bind(name, to_class=implementation_class,  in_scope=pinject.SINGLETON if singleton else pinject.PROTOTYPE)
                bind(convert(name), to_class=implementation_class,  in_scope=pinject.SINGLETON if singleton else pinject.PROTOTYPE)

        spec = SomeBindingSpec(names, register)

        def provider():

            self.object_graph.inject_method(implementation_class, *args, **kwargs)()


        map(lambda name: monkey_patch_instance(spec, "provide_{}".format(name), provider), names)
        map(lambda name: setattr(SomeBindingSpec, "provide_{}".format(name), provider), names)

        self._arg_mappings[implementation_class.__name__] = (args if args else (), kwargs if kwargs else {})

        self._binding_specs.append(spec)

    def load_class(self, clazz):
        clazz = self._class_mappings.get(clazz.__name__, clazz)
        args, kwargs = self._arg_mappings[clazz.__name__]
        return self.object_graph.inject_method(clazz, *args, **kwargs)()

