import pinject
from lazy import lazy
import types
import functools
import inspect
import re
import sys
import pinject.bindings
from threading import Lock
import tdash as _
import pinject.arg_binding_keys as arg_binding_keys


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
        sl = _.result(service_loaders.get(name, lambda: ServiceLoader(name)))
    return sl


def handle_provider_error(implementation_class, injected, exception):
    isclass = inspect.isclass(injected.func)
    fn = injected.func.__init__ if isclass else injected.func
    required,__,___,defaults = inspect.getargspec(fn)
    if defaults:
        required = required[0:-len(defaults)]
    provided = required[0:len(injected.args)]
    provided += injected.keywords.keys()

    raise Exception("Error instantiating class {0} \nRequired: {1} \nProvided: {2} \nError:{3}".format(implementation_class.__name__ , str(required), str(provided), str(exception))), None, sys.exc_info()[2]


class ServiceLoader():
    def __init__(self, name):
        if name in service_loaders:
            raise Exception("cannot instantiate multiple service loaders with same name")
        service_loaders[name] = self

        self._object_graph_initialised = False
        self._binding_specs = []
        self._class_mappings = {}
        self._function_mappings = {}
        self._class_arg_mappings = {}
        self._classes = []
        self._modules = set()

    @lazy
    def object_graph(self):
        """
        :type
        Returns:

        """

        og = pinject.new_object_graph(binding_specs=self._binding_specs, modules=list(self._modules), classes=self._classes)

        def call_with_injection(self, fn, *direct_pargs, **direct_kwargs):
            return self._obj_provider.call_with_injection(fn, self._injection_context_factory.new(fn), direct_pargs, direct_kwargs)

        def provide_class(self, clazz, *args, **kwargs):

            isclass = inspect.isclass(clazz)
            assert isclass
            arg_binding_key = arg_binding_keys.new(convert(clazz.__name__))
            injection_context = self._injection_context_factory.new(clazz.__init__)

            c = self._obj_provider.provide_from_arg_binding_key(clazz, arg_binding_key, injection_context, pargs=args, kwargs=kwargs)
            return c #self._obj_provider.provide_class(c, injection_context, direct_init_pargs=args, direct_init_kwargs=kwargs)

        def inject_method(self, fn, *args, **kwargs):
            isclass = inspect.isclass(fn)
            fn_to_call = fn.__init__ if isclass else fn
            injection_context = self._injection_context_factory.new(fn_to_call)

            pargs, kwargs = self._obj_provider.get_injection_pargs_kwargs(fn_to_call, injection_context, args, kwargs)
            print "Injecting", fn
            print "pargs", pargs
            print "kwargs", kwargs

            return functools.partial(fn, *pargs, **kwargs)

        ## MONKEY PATCHING HAHAHAHA
        monkey_patch_instance(og, 'call_with_injection', call_with_injection)
        monkey_patch_instance(og, 'inject_method', inject_method)
        monkey_patch_instance(og, 'provide_class', provide_class)

        self._object_graph_initialised = True
        return og

    def register_function(self, fn, with_name=None, kwargs={}):
        """
        We deliberately don't take an args param because we think it is safer. If you must provide positional args then explicitly curry your function using partial
        Args:
            fn:
            with_name:
            kwargs:

        """
        assert inspect.isfunction(fn)
        name = with_name if with_name else fn.__name__

        this = self
        # Here we dynamically create a class that conforms to pinject's requirements
        def provider(self):
            return this.object_graph.inject_method(fn, **kwargs)
        self.add_provider(name, provider, singleton=True)

        self._function_mappings[name] = (fn, kwargs)

    def register_module(self, module):
        assert isinstance(module, types.ModuleType)
        self._modules.add(module)

    def register_modules(self, modules):
        modules = set(modules)
        assert all((isinstance(module, types.ModuleType) for module in modules))
        self._modules.update(modules)

    def add_provider(self, name, provider, singleton):
        """

        Args:
            name:
            provider:
            :type provider: function
            singleton:

        Returns:

        """
        fn_name = "provide_{}".format(name)
        provider.__name__ = fn_name
        provider = pinject.provides(in_scope=pinject.PROTOTYPE)(provider) if not singleton else provider
        provider_spec = type('BindingSpec{}'.format(len(self._binding_specs)), (pinject.BindingSpec,), {fn_name: provider})
        provider_spec = provider_spec()
        self._binding_specs.append(provider_spec)



    def register_implementation(self, implementation_class, register_super_classes=True, with_name=None, singleton=False, args=(), kwargs={}):
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

        if register_super_classes:
            names += [clazz.__name__ for clazz in inspect.getmro(implementation_class) if inspect.isclass(clazz)]

        names += [name.replace('Base','').replace('Abstract','') for name in names if name.startswith('Base') or name.startswith('Abstract')]

        names = list(set(names) - {'object'})
        map(lambda name: self._class_mappings.update({name:implementation_class}), names)

        print "Registering {} for :".format(implementation_class), names

        #def register(bind, require):
        #     bind(convert(implementation_class.__name__), to_class=implementation_class,  in_scope=pinject.SINGLETON if singleton else pinject.PROTOTYPE)
        #        name = convert(name)
                #bind(name, to_class=implementation_class,  in_scope=pinject.SINGLETON if singleton else pinject.PROTOTYPE)
        #        print "binding class", name
        #spec = SomeBindingSpec(names, register)
        #self._binding_specs.append(spec)

        this = self

        for name in (convert(name) for name in names if not name == implementation_class.__name__):
            # Here we dynamically create a class that conforms to pinject's requirements
            def provider(self):
                args, kwargs = this._class_arg_mappings[implementation_class.__name__]
                return this.object_graph.provide_class(implementation_class, *args, **kwargs)
            self.add_provider(name, provider, singleton)

        for name in (convert(name) for name in names if name == implementation_class.__name__):
            # Here we dynamically create a class that conforms to pinject's requirements
            def provider(self, **kwargs):
                args, kwargs = this._class_arg_mappings[implementation_class.__name__]
                try:
                    injected = this.object_graph.inject_method(implementation_class, *args, **kwargs)
                    return injected()
                except TypeError as e:
                    handle_provider_error(implementation_class, injected, e)

            self.add_provider(name, provider, singleton)

        self._class_arg_mappings[implementation_class.__name__] = (args if args else (), kwargs if kwargs else {})



    def load_class(self, clazz):
        clazz = self._class_mappings.get(clazz.__name__, clazz)
        args, kwargs = self._class_arg_mappings[clazz.__name__]
        return self.object_graph.provide_class(clazz, *args, **kwargs)

    def apply(self, fn_name, *args, **kwargs):
        fn, config_kwargs = self._function_mappings[fn_name]
        kwargs.update(config_kwargs)
        return self.object_graph.inject_method(fn, *args, **kwargs)()