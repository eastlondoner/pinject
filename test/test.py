
from serviceloader.ServiceLoader import fetch_service_loader

from namedclass import *
from functions import *




sl = fetch_service_loader('error_handling')

sl.register_implementation(ErrorCausingClass)
sl.register_implementation(ErrorDependentClass)
sl.register_implementation(NeedyClassWhichCausesError)

error_occured = False
try:
    implementation_1 = sl.load_class(BaseNeedyClass)
except Exception, e:
    error_occured = True
    assert "Error instantiating class ErrorCausingClass" in e.message

assert error_occured



sl = fetch_service_loader('main')
sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClass, kwargs=dict(data="hi"))

assert sl.load_class(BaseNeedyClass)
assert sl.load_class(NeedyClass)



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


sl = fetch_service_loader('class_in_module')

import moduleclasses
sl.register_module(moduleclasses)
sl.register_implementation(NeedyClassWhichNeedsClassInModule)

assert sl.load_class(BaseNeedyClass)

sl = fetch_service_loader('function_injection')

sl.register_implementation(NeedyClassWhichNeedsFunction)
sl.register_function(hello_world)

assert sl.load_class(BaseNeedyClass)
sl.apply("hello_world")

sl = fetch_service_loader('function_injection_2')

sl.register_implementation(NeedyClassWhichNeedsFunctionInjection)
sl.register_function(hello_from)
sl.register_function(hello_world)

assert sl.load_class(BaseNeedyClass)
sl.apply("hello_world")
sl.apply("hello_from", 'bob')

sl = fetch_service_loader('function_injection_3')

sl.register_implementation(NeedyClassWhichNeedsCurriedFunction)
sl.register_function(hello_from, kwargs=dict(name='jane'))
sl.register_function(hello_world)

assert sl.load_class(BaseNeedyClass)
sl.apply("hello_world")


sl = fetch_service_loader('not_singleton')

sl.register_implementation(SimpleNeedyClass)
sl.register_implementation(NamedClass)

implementation_1 = sl.load_class(BaseNeedyClass)
implementation_2 = sl.load_class(BaseNeedyClass)
assert implementation_1.thing is not implementation_2.thing

sl = fetch_service_loader('singleton_dependency')

sl.register_implementation(SimpleNeedyClass)
sl.register_implementation(NamedClass, singleton=True)

implementation_1 = sl.load_class(BaseNeedyClass)
implementation_2 = sl.load_class(BaseNeedyClass)
thing_3 = sl.load_class(NamedClass)
assert implementation_1.thing is implementation_2.thing
assert implementation_1.thing is thing_3


sl = fetch_service_loader('singleton_top_level')

sl.register_implementation(NamedClass, singleton=True)

implementation_1 = sl.load_class(NamedClass)
implementation_2 = sl.load_class(NamedClass)
implementation_3 = sl.load_class(BaseThing)
assert implementation_1 is implementation_2
assert implementation_2 is implementation_3




"""
sl = fetch_service_loader('function_in_module')

sl.register_module(moduleclasses)
sl.register_implementation(NeedyClassWhichNeedsFunctionInModule)

assert sl.load_class(BaseNeedyClass)
"""