from datetime import datetime
from decimal import *
import re
import numpy as np

# SORT :: [Sensor_agent] -> Integer -> [Sensor_agent]
# Given a list xs and int i returns xs sorted according to i
sort = lambda xs, i: xs.sort(key=lambda x: x[i])

# MEAN :: List -> Decimal
# Given a list xs returns a list of the mean values on axis 0
mean = lambda xs: np.mean(xs)

# STD :: List -> Decimal
# Given a list xs returns a list of the standard deviation values on axis 0
std = lambda xs: np.std(xs)

# INTERVALS :: List -> [List]
# Given a list xs returns a list of the items in xs grouped into discovered intervals as lists
def intervals(xs):
    for sa in xs:
        

# BASIC MATH <not yet implemented>

# ADD :: int -> int
add = lambda n : n + 1

# SUBTRACT :: int -> int
subtract = lambda n : n - 1

# DOUBLE :: int -> int
double = lambda n : n * 2

# HALF :: int -> int
half = lambda n : n / 2

# UPRAISE :: int -> int
upraise = lambda n : n **2

# DSL Method index
method = {
0: [sort, ['list', 'int'], 'list'],
1: [mean, ['list'], 'Decimal'],
2: [std, ['list'], 'Decimal']
}

# TESTING
def test_methods():
    input = '10017 10209 1523779635 22.3 61 data3'

#test_methods()
