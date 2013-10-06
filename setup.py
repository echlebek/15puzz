#!/usr/bin/env python

from distutils.core import setup, Command
from distutils.extension import Extension
import os
import numpy as np
from Cython.Distutils import build_ext
from unittest import TextTestRunner, TestLoader


os.environ['TEST_DATA_ROOT'] = os.path.abspath("tests/data")


class UnitTest(Command):
    def run(self):
        import tests.unit.test_15p
        loader = TestLoader()
        t = TextTestRunner()
        t.run(loader.loadTestsFromModule(tests.unit.test_15p))

    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

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
    cmdclass={"cram": CramTest, "build_ext": build_ext, "test": UnitTest},
    ext_modules=[
        Extension("_c15", ["fifteen/_c15.pyx"], [np.get_include()])
    ]
)
