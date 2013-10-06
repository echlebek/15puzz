#!/usr/bin/env python

from distutils.core import setup, Command
from distutils.extension import Extension
import os
import numpy as np
from Cython.Distutils import build_ext


os.environ['TEST_DATA_ROOT'] = os.path.abspath("tests/data")


class CramTest(Command):
    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        import cram
        import sys

        test_root = os.path.abspath("tests/cram")
        tests = [os.path.join(test_root, test) for test in os.listdir("tests/cram")]

        sys.exit(cram.main(tests))


setup(
    name="15puzz",
    version="0.0.0",
    description="15 Puzzle Game",
    author="Eric Chlebek",
    author_email="echlebek@gmail.com",
    packages=["fifteen"],
    #scripts=["scripts/15puzz"],
    test_suite="tests.unit",
    cmdclass={"cram": CramTest, "build_ext": build_ext},
    ext_modules=[
        Extension("_c15", ["fifteen/_c15.pyx"], [np.get_include()])
    ]
)
