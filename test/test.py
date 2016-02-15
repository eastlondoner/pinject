
from serviceloader.ServiceLoader import fetch_service_loader

from namedclass import *

sl = fetch_service_loader('main')

sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClass, kwargs=dict(data="hi"))

assert sl.load_class(BaseNeedyClass)



sl = fetch_service_loader('base_convention')

sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClassWithConvention)

assert sl.load_class(BaseNeedyClass)
print "passed convention"

sl = fetch_service_loader('with_name')

sl.register_implementation(NamedClass, with_name="funky_thing")
sl.register_implementation(NeedyClassWithFunnyNamedArg)

assert sl.load_class(BaseNeedyClass)


sl = fetch_service_loader('optional_named_thing')

sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClassWithOptionalArg)

assert sl.load_class(BaseNeedyClass)