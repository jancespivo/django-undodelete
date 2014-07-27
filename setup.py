# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGE = "django-undodelete"
NAME = "django-undodelete"
DESCRIPTION = "Undo support for Django models"
AUTHOR = "Jan Češpivo (http://www.cespivo.cz)"
AUTHOR_EMAIL = "jan.cespivo@gmail.com"
URL = "https://github.com/cespivo/django-undodelete"
VERSION = '0.0.1a'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="LICENSE",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: LGPLv3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "",
    ],
)
