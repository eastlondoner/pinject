import functools


class OtherThing(object):
    def __init__(self):
        pass

class BaseThing(object):
    def __init__(self):
        pass


class NamedClass(BaseThing):
    def __init__(self):
        super(NamedClass, self).__init__()


class NamedClassExtendsDict(dict):
    pass

class ExtendsDict(dict):
    pass

class NamedClassExtendsExtendsDict(NamedClassExtendsDict):
    def __init__(self, mock_values):
        for k,v in mock_values.iteritems():
            self[k] = v


class DependsOnExtendsDict(object):
    def __init__(self, named_class_extends_extends_dict):
        self.foo = named_class_extends_extends_dict

class ErrorCausingClass(BaseThing):
    def __init__(self, other):
        super(ErrorCausingClass, self).__init__()
        thing = 5
        thing = thin * 2

class ErrorDependentClass(object):
    def __init__(self, error_causing_class):
        pass

class BaseNeedyClass(object):
    def __init__(self):
        pass


class SimpleNeedyClass(BaseNeedyClass):

    def __init__(self, thing):
        super(BaseNeedyClass, self).__init__()
        assert thing
        self.thing = thing


class NeedyClass(BaseNeedyClass):

    def __init__(self, data, base_thing,
                 optional_value=None):
        super(BaseNeedyClass, self).__init__()
        assert data
        assert base_thing
        print data
        print base_thing
        self.optional_value = optional_value
        print self.optional_value


class NeedyClassWithConvention(BaseNeedyClass):

    def __init__(self, thing,
                 optional_value=None):
        super(BaseNeedyClass, self).__init__()
        print thing
        assert thing


class NeedyClassWithFunnyNamedArg(BaseNeedyClass):

    def __init__(self, funky_thing):
        super(BaseNeedyClass, self).__init__()
        print funky_thing
        assert funky_thing

class NeedyClassWithOptionalArg(BaseNeedyClass):

    def __init__(self, thing=None):
        super(BaseNeedyClass, self).__init__()
        print thing
        assert thing


class NeedyClassWhichNeedsClassInModule(BaseNeedyClass):

    def __init__(self, class_in_module=None):
        super(BaseNeedyClass, self).__init__()
        print class_in_module
        assert class_in_module

class NeedyClassWhichNeedsFunction(BaseNeedyClass):
    def __init__(self, hello_world):
        super(BaseNeedyClass, self).__init__()
        hello_world()

class NeedyClassWhichNeedsFunctionInjection(BaseNeedyClass):
    def __init__(self, hello_from):
        super(BaseNeedyClass, self).__init__()
        self._injected = functools.partial(hello_from, 'dave')
        self._injected()
    def call_injected(self):
        return self._injected()

class NeedyClassWhichNeedsCurriedFunction(BaseNeedyClass):
    def __init__(self, hello_from):
        super(BaseNeedyClass, self).__init__()
        hello_from()
        self.hello_from = hello_from
    def call_curried(self):
        return self.hello_from()



class NeedyClassWhichNeedsFunctionInModule(BaseNeedyClass):

    def __init__(self, function_in_module=None):
        super(BaseNeedyClass, self).__init__()
        print function_in_module
        assert function_in_module



class NeedyClassWhichCausesError(BaseNeedyClass):

    def __init__(self, error_dependent_class):
        assert False # we should never get here
        super(BaseNeedyClass, self).__init__()

class DependsOnNeedyClass(object):
    def __init__(self, needy_class):
        assert needy_class

class InheritsNeedyClassUsesKwargsDirectly(NeedyClass):
    def __init__(self, **kwargs):
        print 'kwargs', kwargs
        super(InheritsNeedyClassUsesKwargsDirectly, self).__init__(**kwargs)

class InheritsNeedyClassUsesKwargsConvention(NeedyClassWithConvention):
    def __init__(self, **kwargs):
        print 'kwargs', kwargs
        super(InheritsNeedyClassUsesKwargsConvention, self).__init__(**kwargs)

class NeedyClassWithConvention(BaseNeedyClass):
    def __init__(self, thing,
                 optional_value=None):
        super(BaseNeedyClass, self).__init__()
        print thing
        assert thing

class InheritsNeedyClassUsesSomeKwargs(NeedyClassWithConvention):
    def __init__(self, other_thing, **kwargs):
        print 'kwargs', kwargs
        super(InheritsNeedyClassUsesSomeKwargs, self).__init__(**kwargs)
        assert other_thing