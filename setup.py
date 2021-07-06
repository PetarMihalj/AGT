import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "agtc",
    version = read("VERSION"),
    author = "Petar Mihalj",
    author_email = "agt@pmihalj.com",
    description = ("Compiler for AGT programming language"),

    license = "MIT",
    keywords = "agt agtc compiler",
    url = "https://github.com/PetarMihalj/AGT",
    packages = find_packages(),
    long_description = read("README.md"),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
    ],
    setup_requires = [
        "pytest-runner",
    ],
    install_requires = [
        "ply>=3.11",
        "pytest>=6.2.4",
        "click>=7.0.0",
    ]
)
