#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from distutils.core import setup

from basagc import config

setup(
    name='basaGC',
    version=config.VERSION,
    packages=['basagc'],
    url=config.WEBSITE,
    license='GPL',
    author=config.DEVELOPERS,
    author_email='cashelcomputers@gmail.com',
    description='A implementation of the Apollo Guidance Computer for Kerbal Space Program',
    requires=['PyQt5', ]
)
