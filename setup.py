#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import os


os.environ['TEST_DATA_ROOT'] = os.path.abspath("tests/data")


class CramTest(TestCommand):

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
    cmdclass={"cram": CramTest},
    install_requires=["numpy", "cython"]
)
