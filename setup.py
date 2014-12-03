#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from basagc import config

from distutils.core import setup

setup(
    name='basaGC',
    version=config.VERSION,
    packages=['basagc'],
    url=config.WEBSITE,
    license='GPL',
    author=config.DEVELOPERS,
    author_email='cashelcomputers@gmail.com',
    description='A implementation of the Apollo Guidance Computer for Kerbal Space Program',
    requires=[]
)
