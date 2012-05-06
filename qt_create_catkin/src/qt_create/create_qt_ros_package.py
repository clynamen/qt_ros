import roslib; 
roslib.load_manifest('roscreate')
roslib.load_manifest('qt_create')

# This sets up a typical qt-based ros package.

import os
import sys
import shutil
import roslib.packages
from roscreate.core import author_name
from qt_create.core import read_template
from qt_create.core import instantiate_template

def get_qt_text_templates(package):
    template_dir = os.path.join(roslib.packages.get_pkg_dir('qt_create'),'templates','qt-ros')
    templates = {}
    templates['mainpage.dox'] = read_template(os.path.join(template_dir,'mainpage.dox'))
    templates['Makefile'] = read_template(os.path.join(template_dir,'Makefile'))
    templates['CMakeLists.txt'] = read_template(os.path.join(template_dir,'CMakeLists.txt'))
    templates['rosbuild.cmake'] = read_template(os.path.join(template_dir,'rosbuild.cmake'))
    templates['manifest.xml'] = read_template(os.path.join(template_dir,'manifest.xml'))
    templates[os.path.join('ui','main_window.ui')] = read_template(os.path.join(template_dir,'ui','main_window.ui'))
    templates[os.path.join('src','main.cpp')] = read_template(os.path.join(template_dir,'src','main.cpp'))
    templates[os.path.join('src','main_window.cpp')] = read_template(os.path.join(template_dir,'src','main_window.cpp'))
    templates[os.path.join('src','qnode.cpp')] = read_template(os.path.join(template_dir,'src','qnode.cpp'))
    templates[os.path.join('resources','images.qrc')] = read_template(os.path.join(template_dir,'resources','images.qrc'))
    templates[os.path.join('include',package,'main_window.hpp')] = read_template(os.path.join(template_dir,'include','PACKAGE_NAME','main_window.hpp'))
    templates[os.path.join('include',package,'qnode.hpp')] = read_template(os.path.join(template_dir,'include','PACKAGE_NAME','qnode.hpp'))
    return templates

def create_qt_package(package, depends):
    
    p = os.path.abspath(package)
    os.makedirs(os.path.join(p,"src"))
    os.makedirs(os.path.join(p,"include"))
    os.makedirs(os.path.join(p,"include",package))
    os.makedirs(os.path.join(p,"resources"))
    os.makedirs(os.path.join(p,"resources","images"))
    os.makedirs(os.path.join(p,"ui"))
    print "Created qt package directories."

    # Qt text files
    templates = get_qt_text_templates(package)
    for filename, template in templates.iteritems():
        contents = instantiate_template(template, package, package, package, author_name(), depends)
        try:
            p = os.path.abspath(os.path.join(package, filename))
            f = open(p, 'w')
            f.write(contents)
            print "Created package file", p
        finally:
            f.close()
    # Qt binary files
    template_dir = os.path.join(roslib.packages.get_pkg_dir('qt_create'),'templates','qt-ros')
    shutil.copy(os.path.join(template_dir,'resources','images','icon.png'),
                os.path.join(os.path.abspath(package),'resources','images','icon.png'))
    

def main(catkin=True):
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog <package-name> [dependencies...]")
    options, args = parser.parse_args()
    if not args:
        parser.error("you must specify a package name and optionally also list package dependencies")
    package = args[0]

    # validate dependencies and turn into XML
    depends = args[1:]

    for d in depends:
        try:
            roslib.packages.get_pkg_dir(d)
        except roslib.packages.InvalidROSPkgException:
            print >> sys.stderr, "ERROR: dependency [%s] cannot be found"%d
            sys.exit(1)
    depends = ''.join(['  <depend package="%s"/>\n'%d for d in depends])

    create_qt_package(package, depends, catkin )
    print "\nPlease edit %s/manifest.xml and mainpage.dox to finish creating your package"%package

if __name__ == "__main__":
    main()