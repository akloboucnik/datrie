#! /usr/bin/env python
"""Super-fast, efficiently stored Trie for Python."""

import glob
import os
import subprocess

from setuptools import setup, Extension
import Cython.Build

LIBDATRIE_DIR = 'libdatrie'
LIBDATRIE_FILES = sorted(glob.glob(os.path.join(LIBDATRIE_DIR, "datrie", "*.c")))

DESCRIPTION = __doc__
LONG_DESCRIPTION = open('README.rst').read() + open('CHANGES.rst').read()
LICENSE = 'LGPLv2+'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'Programming Language :: Cython',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing :: Linguistic'
]

extensions = [
        Extension("datrie", [
            'src/datrie.c',
            'src/cdatrie.c',
            'src/stdio_ext.c'
            ])
        ]

ext_modules = Cython.Build.cythonize(
    'src/datrie.pyx', 'src/cdatrie.pxd', 'src/stdio_ext.pxd',
    annotate=True,
    include_path=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")]
    )

for m in ext_modules:
    m.include_dirs=[LIBDATRIE_DIR]

proc = subprocess.Popen(['rm', '-rf', './libdatrie'],
                        stdout=subprocess.PIPE)
status, _ = proc.communicate()
status = status.decode("ascii", "replace")
print(status)

proc = subprocess.Popen(['git', 'clone', 'https://github.com/tlwg/libdatrie.git'],
                        stdout=subprocess.PIPE)
status, _ = proc.communicate()
status = status.decode("ascii", "replace")
print(status)

setup(name="datrie",
      version="0.7.1",
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='Mikhail Korobov',
      author_email='kmike84@gmail.com',
      license=LICENSE,
      url='https://github.com/kmike/datrie',
      classifiers=CLASSIFIERS,
      libraries=[('libdatrie', {
          "sources": LIBDATRIE_FILES,
          "include_dirs": [LIBDATRIE_DIR]})],
      ext_modules=Cython.Build.cythonize(ext_modules),
      setup_requires=["pytest-runner", "cython>=0.28"],
      tests_require=["pytest", "hypothesis"])
