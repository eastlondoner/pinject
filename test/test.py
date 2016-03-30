
from serviceloader.ServiceLoader import fetch_service_loader

from namedclass import *
from functions import *


sl = fetch_service_loader('error_handling')

sl.register_implementation(ErrorCausingClass)
sl.register_implementation(ErrorDependentClass)
sl.register_implementation(NeedyClassWhichCausesError)
sl.register_implementation(DependsOnNeedyClass)

error_occured = False
try:
    implementation_1 = sl.load_class(BaseNeedyClass)
except Exception, e:
    error_occured = True
    print e.message
    assert "Error instantiating class ErrorCausingClass" in e.message

assert error_occured

error_occured = False
try:
    implementation_1 = sl.load_class(DependsOnNeedyClass)
except Exception, e:
    error_occured = True
    assert "Error instantiating class ErrorCausingClass" in e.message

assert error_occured


sl = fetch_service_loader('main')
sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClass, kwargs=dict(data="hi"))
sl.register_implementation(DependsOnNeedyClass)

assert sl.load_class(BaseNeedyClass)
assert sl.load_class(NeedyClass)
assert sl.load_class(DependsOnNeedyClass)


sl = fetch_service_loader('base_convention')

sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClassWithConvention)
sl.register_implementation(DependsOnNeedyClass)

assert sl.load_class(BaseNeedyClass)
assert sl.load_class(DependsOnNeedyClass)


sl = fetch_service_loader('with_name')

sl.register_implementation(NamedClass, with_name="funky_thing")
sl.register_implementation(NeedyClassWithFunnyNamedArg)
sl.register_implementation(DependsOnNeedyClass)

assert sl.load_class(BaseNeedyClass)
assert sl.load_class(DependsOnNeedyClass)


sl = fetch_service_loader('optional_named_thing')

sl.register_implementation(NamedClass)
sl.register_implementation(NeedyClassWithOptionalArg)
sl.register_implementation(DependsOnNeedyClass)

assert sl.load_class(BaseNeedyClass)
assert sl.load_class(DependsOnNeedyClass)


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
assert sl.apply("hello_from", 'bob') == 'bob'
assert 'dave' in sl.load_class(NeedyClassWhichNeedsFunctionInjection).call_injected()

sl = fetch_service_loader('function_injection_3')

sl.register_implementation(NeedyClassWhichNeedsCurriedFunction)
sl.register_function(hello_from, kwargs=dict(name='jane'))
sl.register_function(hello_world)
sl.register_implementation(DependsOnNeedyClass)

assert sl.load_class(BaseNeedyClass)
sl.apply("hello_world")
assert sl.load_class(DependsOnNeedyClass)
assert 'jane' in sl.load_class(NeedyClassWhichNeedsCurriedFunction).call_curried()

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

sl = fetch_service_loader('partial_application')

sl.register_implementation(DependsOnNeedyClass)
sl.register_implementation(NeedyClass, register_super_classes=True, kwargs=dict(data='hi'))
sl.register_implementation(BaseThing)

implementation = sl.load_class(DependsOnNeedyClass)



sl = fetch_service_loader('kwargs in inheritance')
sl.register_implementation(NamedClass)
sl.register_implementation(InheritsNeedyClassUsesKwargsDirectly, kwargs=dict(data="hi"))

assert sl.load_class(InheritsNeedyClassUsesKwargsDirectly)



sl = fetch_service_loader('kwargs in inheritance 2')
sl.register_implementation(NamedClass)
sl.register_implementation(InheritsNeedyClassUsesKwargsConvention)

assert sl.load_class(InheritsNeedyClassUsesKwargsConvention)



sl = fetch_service_loader('kwargs in inheritance 3')
sl.register_implementation(NamedClass)
sl.register_implementation(InheritsNeedyClassUsesKwargsConvention)
sl.register_implementation(DependsOnNeedyClass)

assert sl.load_class(DependsOnNeedyClass)



sl = fetch_service_loader('kwargs in inheritance 4')
sl.register_implementation(NamedClass)
sl.register_implementation(OtherThing)
sl.register_implementation(InheritsNeedyClassUsesSomeKwargs)
sl.register_implementation(DependsOnNeedyClass)
sl.register_module(moduleclasses)

assert sl.load_class(InheritsNeedyClassUsesSomeKwargs)
assert sl.load_class(DependsOnNeedyClass)


sl = fetch_service_loader('dict in inheritance')
mock_values = {'snapshot_details': {'snapshot_path': 'features'}}
sl.register_implementation(NamedClassExtendsExtendsDict, kwargs={'mock_values': mock_values}, singleton=True)
sl.register_implementation(DependsOnExtendsDict)

assert sl.load_class(DependsOnExtendsDict)
assert sl.load_class(NamedClassExtendsExtendsDict)['snapshot_details']




"""
sl = fetch_service_loader('function_in_module')

sl.register_module(moduleclasses)
sl.register_implementation(NeedyClassWhichNeedsFunctionInModule)

assert sl.load_class(BaseNeedyClass)
"""