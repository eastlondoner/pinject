
from serviceloader.ServiceLoader import fetch_service_loader

from namedclass import *
from functions import *

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




"""
sl = fetch_service_loader('function_in_module')

sl.register_module(moduleclasses)
sl.register_implementation(NeedyClassWhichNeedsFunctionInModule)

assert sl.load_class(BaseNeedyClass)
"""