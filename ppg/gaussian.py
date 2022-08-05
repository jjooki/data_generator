# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:26:00 2021

@author: jjooki

This file is a set of gaussian function.

"""

import math

# Gaussian distribution function
def dist(mu, sigma, x):
    return math.exp(- (x - mu) ** 2 / 2 / sigma ** 2) / math.sqrt(2 * math.pi) / sigma

# Gaussian function general form
def func(A, mu, sigma, x):
    return A * math.exp(-(x - mu) ** 2 / 2 / sigma ** 2)

# Accumulated possibility (X <= x) of gaussian distribution
def accum_p_dist(mu, sigma, x):
    return (1 + math.erf((x - mu) / sigma / math.sqrt(2))) / 2