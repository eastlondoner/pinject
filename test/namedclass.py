
class BaseThing(object):
    def __init__(self):
        pass


class NamedClass(BaseThing):
    def __init__(self):
        super(NamedClass, self).__init__()


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
        hello_from('dave')

class NeedyClassWhichNeedsCurriedFunction(BaseNeedyClass):
    def __init__(self, hello_from):
        super(BaseNeedyClass, self).__init__()
        hello_from()



class NeedyClassWhichNeedsFunctionInModule(BaseNeedyClass):

    def __init__(self, function_in_module=None):
        super(BaseNeedyClass, self).__init__()
        print function_in_module
        assert function_in_module



class NeedyClassWhichCausesError(BaseNeedyClass):

    def __init__(self, error_dependent_class):
        assert False # we should never get here
        super(BaseNeedyClass, self).__init__()