#!/usr/bin/env python3
""" This file contains vector math."""

import math

def cross_product(x, y):
    return x[1]*y[2] - x[2]*y[1], x[2]*y[0] - x[0]*y[2], x[0]*y[1] - x[1]*y[0]

def dot_product(x, y):
    return x[0]*y[0] + x[1]*y[1] + x[2]*y[2]

def magnitude(x):
    return math.sqrt(x[0]**2 + x[1]**2 + x[2]**2)

def angle_between_vectors(x, y):
    """ Compute the angle between vector x and y """
    dp = dot_product(x, y)
    if dp == 0:
        return 0
    xm = magnitude(x)
    ym = magnitude(y)
    return math.acos(dp / (xm*ym)) * (180. / math.pi)

def angle_between_vector_and_plane(x, n):
    """ Compute the angle between a vector x and plane with normal vector n """
    dp = dot_product(x,n)
    if dp == 0:
        return 0
    xm = magnitude(x)
    nm = magnitude(n)
    return math.asin(dp / (xm*nm)) * (180. / math.pi)