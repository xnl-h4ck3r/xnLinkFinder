#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="xnLinkFinder",
    packages=find_packages(),
    version="0.1",
    description="A python script to find endpoints from the from a URL, file of URLsm or a Burp xml file.",
    long_description=open("README.md").read(),
    author="@xnl-h4ck3r",
    url="https://github.com/xnl-h4ck3r/xnlLinkFinder",
    py_modules=["xnLinkFinder"],
    install_requires=["argparse","requests","psutil"],
)
