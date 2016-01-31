#!/usr/bin/env python

#import sys
import setuptools
#from distutils.extension import Extension
#import os

# setuptools DWIM monkey-patch madness
# http://mail.python.org/pipermail/distutils-sig/2007-September/thread.html#8204
#if 'setuptools.extension' in sys.modules:
#    m = sys.modules['setuptools.extension']
#    m.Extension.__dict__ = m._Extension.__dict__


setuptools.setup(name='droneRace',
                 version='1.0.0',
                 description='Drone Race',
                 author='Linus Casassa',
                 author_email='lcasassa@gmail.com',
                 packages=setuptools.find_packages(),
                 entry_points={
                     'console_scripts': [
                         'droneRace = droneRace.droneRace:main'
                     ]
                 },
                 # install_requires=['', ''],
                 include_package_data=True,
                 zip_safe=False
                 )

print("Done")
