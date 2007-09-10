#! /usr/bin/env python
#
# Copyright 2007 Nicolas Rougier
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Package builder for scons 

Example usage (from you Sconstruct file):
-----------------------------------------

from package import Files, package_builder

...
 
env.Append (BUILDERS = {'Package' : package_builder})

...


"""

from SCons.Script import *
import shutil

# _______________________________________________________________________Package
def Package (target, source, env):
    """ Make a package from sources """

    name        = str(target[0])
    path        = name + '.tmp'

    # Remove build tree if it exists
    shutil.rmtree (path, ignore_errors=True)

    files = []
    installs = env["INSTALLS"]
    for i in installs:
        files.append ( [str(i).replace (env["PREFIX"]+'/', ''),
                        str(i.sources[0])])

    package_size = 0
    for f in files:
        dest = os.path.join(path, 'usr', f[0])
        subdirs = os.path.dirname(dest).split('/')
        dir = ''
        for d in subdirs:
            dir = os.path.join (dir, d)
            if not os.path.exists (dir):
                os.mkdir (dir)
        shutil.copy (f[1], dest)
        package_size += os.path.getsize (f[1])

    CONTROL_TEMPLATE = """
Package: %s
Priority: extra
Section: misc
Installed-Size: %s
Maintainer: %s
Architecture: %s
Version: %s
Depends: %s
Description: %s
"""
    control_info = CONTROL_TEMPLATE % (
        env['PACKAGE_NAME'],
        package_size,
        env['MAINTAINER'],
        env['ARCH'],
        env['PACKAGE_VERSION'],
        env['DEPENDENCIES'],
        env['DESCRIPTION'])
    os.mkdir (os.path.join (path, 'DEBIAN'))
    f = open (os.path.join (path, 'DEBIAN', 'control'), 'w')
    f.write (control_info)
    f.close()

    os.system ("dpkg-deb -b %s %s" % ("%s" % path, name))



# _________________________________________________________________PackageString
def PackageString (target, source, env):
    """ Information string for Package """

    return "Making package %s" % str(target[0])


package_builder = Builder (action = SCons.Action.Action(Package, PackageString))

