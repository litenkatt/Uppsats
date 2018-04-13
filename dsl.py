from datetime import datetime
from decimal import *

# Constant index :: int
i = 0

# SPLIT :: String -> [String]
# Given a string, returns an array of strings divided by the blankspaces of the original string.
split = lambda s : s.split()

# SIZE :: [String] -> int
# Given an array, returns the number of elements in that array.
size = lambda xs : len(xs)

# INTCONVERT :: String -> int
# Given a string, returns an int.
intconvert = lambda s : int(s)

# DECIMALCONVERT :: String -> decimal
# Given a string, returns a decimal.
decimalconvert = lambda s : Decimal(s)

# DATECONVERT :: decimal -> datetime
# Given a decimal d returns the a datetime object.
dateconvert = lambda d : datetime.fromtimestamp(d)

# LOWERCASE :: String -> String
# Given a string s returns the string converted to all lowercase letters if applicable.
lowercase = lambda s : s.decode('utf-8').lower()

# GET :: int -> [String] -> String
# Given an integer n and array xs, returns the (n+1)-st element of xs.
# (If the length of xs was less than or equal to n, the value NULL is returned instead).
get = lambda n, xs : xs[n] if n>=0 and len(xs)>n else None

# TAKE :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array truncated after the n-th element.
# (If the length of xs was no larger than n in the first place, it is returned without modification.)
take = lambda n, xs : xs[:n]

# DROP :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array with the first n elements dropped.
# (If the length of xs was no larger than n in the first place, an empty array is returned.)
drop = lambda n, xs : xs[n:]

# INSERT :: int -> String ->[String] -> String
# Given an integer n, a String s, and an array xs, inserts s at the (n+1)-st position in xs, replacing the previous value if applicable.
# (If the length of xs was less than or equal to n, the value NULL is returned instead).
def insert(s, n, xs):
    if n >= 0 and len(xs) > n : xs[n] = s
    else : return None
    return xs

# SWITCH :: int -> int -> [int] -> [int]
# Given two integers n1 and n2, and one array xs, returns an array with the elements of index n1 and n2 in switched places.
def switch(n1, n2, xs):
    t = get(n1, xs)
    insert(ACCESS(n2, xs), n1, xs)
    insert(t, n2, xs)
    return xs

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
0: split,
1: size,
2: intconvert,
3: decimalconvert,
4: dateconvert,
5: lowercase,
6: get,
7: take,
8: drop,
9: insert,
10: switch,
11: add,
12: subtract,
13: double,
14: half,
15: upraise
}
