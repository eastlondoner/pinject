#!/usr/bin/env python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from distutils.core import setup


setup(name='serviceloader',
      version='0.10.3',
      description='A variation on a pythonic dependency injection library',
      author='Andrew Jefferson',
      author_email='andrew@tractable.io',
      url='https://github.com/eastlondoner/pinject',
      license='Apache License 2.0',
      long_description=open('README.rst').read(),
      platforms='all',
      packages=['pinject', 'pinject/third_party', 'serviceloader'],
      install_requires=[
      'lazy',
  ])
