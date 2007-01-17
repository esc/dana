#!/usr/bin/env python


# BEFORE importing disutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
import os
if os.path.exists('MANIFEST'): os.remove('MANIFEST')


import glob
from distutils.core import setup, Extension
import distutils.sysconfig
import numpy

# Get core shared object filename
from dana.core._core import __file__ as core
include_dir = core[:core.find('python')]
include_dirs = [os.path.normpath (os.path.join (include_dir, '../include/dana/'))]
include_dirs.append (numpy.get_include())


print '-----------------------------------------------------'
print 'Guessed include directory (based on package core) :'
print ' =>', include_dir
print '     If this is wrong, please modify setup.py'
print '-----------------------------------------------------'
print


life_srcs = glob.glob ("dana/life/*.cc")
life_ext = Extension (
    'dana.life._life',
    sources = life_srcs,
    libraries = ['boost_python'],
    include_dirs =  include_dirs,
    extra_objects=[core]
)


setup (name='dana.life',
       version = '1.0',
       author = 'Nicolas Rougier',
       author_email = 'Nicolas.Rougier@loria.fr',
       url = 'http://www.loria.fr/~rougier',
       description = "DANA: life",
       packages = ['dana.life'],
       ext_modules = [life_ext],
      )