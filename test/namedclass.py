
class BaseThing(object):
    def __init__(self):
        pass


class NamedClass(BaseThing):
    def __init__(self):
        super(NamedClass, self).__init__()


class BaseNeedyClass(object):
    def __init__(self):
        pass


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