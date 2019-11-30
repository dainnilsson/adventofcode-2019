from setuptools import setup, find_packages

setup(
    name="aoc19",
    version="0.1.0",
    description="Python solutions to https://adventofcode.com for 2019",
    url="https://github.com/dainnilsson/adventofcode-2019",
    author="Dain Nilsson",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    packages=find_packages(exclude=["test", "test.*"]),
    test_suite="test",
)
