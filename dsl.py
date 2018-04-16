from datetime import datetime
from decimal import *

# TOString :: Array -> Strings
# Given an array xs returns a string of said Array
to_string = lambda xs : str(xs)

# SPLIT :: String -> [String]
# Given a string, returns an array of strings divided by the blankspaces of the original string.
split = lambda s : s.split()

# SIZE :: [String] -> int
# Given an array, returns the number of elements in that array.
size = lambda xs : len(xs)

# LOWERCASE :: String -> String
# Given a string s returns the string converted to all lowercase letters if applicable.
lowercase = lambda s : s.decode('utf-8').lower()

# GET :: int -> [String] -> String
# Given an integer n and array xs, returns the (n+1)-st element of xs.
# (If the length of xs was less than or equal to n, the value NULL is returned instead).
get = lambda xs, n : xs[n] if n >= 0 and len(xs) > n else None

# TAKE :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array truncated after the n-th element.
# (If the length of xs was no larger than n in the first place, it is returned without modification.)
take = lambda xs, n : xs[:n]

# DROP :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array with the first n elements dropped.
# (If the length of xs was no larger than n in the first place, an empty array is returned.)
drop = lambda xs, n : xs[n:]

# CONVERT_DATA :: [String] -> Array
# Given an array of strings xs, returns an array of Strings, Integers, and or floats.
def convert_data(xs):
    for i in range(len(xs)):
        e = xs[i]
        if isinstance(e, str):
            if e.isdigit():
                xs[i] = int(e)
                try:
                    d = datetime.fromtimestamp(xs[i])
                    dt = datetime.now()
                    if d.year == dt.year and d.month == dt.month : xs[i] = d
                except OSError: continue
            else:
                try: xs[i] = float(e)
                except ValueError: continue
    return xs

# INSERT :: int -> [object] ->[String] -> [String]
# Given an integer n, an object o or array, and an array xs, inserts s at the (n+1)-st position in xs, replacing the previous value if applicable
# and returns the new xs. (If the length of xs was less than or equal to n, the value NULL is returned instead).
def insert(xs, o, n):
    if n >= 0 and len(xs) > n : xs[n] = o
    else : return None
    return xs

# SWITCH :: int -> int -> [int] -> [int]
# Given two integers n1 and n2, and one array xs, returns an array with the elements of index n1 and n2 in switched places.
def switch(xs, n1, n2):
    t = get(xs, n1)
    insert(xs, get(xs, n2), n1)
    insert(xs, t, n2)
    return xs

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
0: [to_string, 1, 'Object'],
1: [split, 1, 'String'],
2: [size, 1, 'Object'],
3: [lowercase, 1, 'String'],
4: [get, 2, ['Array', 'int']],
5: [take, 2, ['Array', 'int']],
6: [drop, 2, ['Array', 'int']],
7: [convert_data, 1, 'Array'],
8: [insert, 3, ['Array', 'Object', 'int']],
9: [switch, 3, ['Array', 'int', 'int']],
}

# TESTING
def test_methods():
    input = '10017 10209 1523779635 22.3 61 data3'
    print ('testing: ' + input)
    key = take(insert(convert_data(split(input)), drop(convert_data(split(input)), 3), 3), 4)
    print ('key : ' + str(key))
    # split
    a = method[1][0](input)
    print ('a : ' + str(a))
    # convert_data
    b = method[7][0](a)
    print ('b : ' + str(b))
    # drop
    c = method[6][0](b, 3)
    print ('c : ' + str(c))
    # insert
    d = method[8][0](b, c, 3)
    print ('d : ' + str(d))
    # take
    e = method[5][0](d, 4)
    # result
    print ('e (result) : ' + str(e))
    print ('Result == key : ' + str(e == key))
    return e

#test_methods()
