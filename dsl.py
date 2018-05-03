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
lowercase = lambda s : s.lower()

# GET :: int -> [String] -> String
# Given an integer n and array xs, returns the (n+1)-st element of xs.
# (If the length of xs was less than or equal to n, the value NULL is returned instead).
get = lambda xs, n : xs[n] if n >= 0 and len(xs) > n else None

# TAKE :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array truncated after the (n+1)-st element.
# (If the length of xs was no larger than n in the first place, it is returned without modification.)
take = lambda xs, n : xs[:(n + 1)]

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
                    if dt.year - d.year <= 1 and (dt.month - d.month <= 1 or dt.month - d.month == 11) : xs[i] = d
                except OSError: continue
            else:
                try: xs[i] = float(e)
                except ValueError: continue
    return xs

# INSERT :: int -> [object] ->[String] -> [String]
# Given an integer n, an object o or array, and an array xs, inserts s at the (n+1)-st position in xs, replacing the previous value if applicable
# and returns the new xs. (If the length of xs was less than or equal to n, the value NULL is returned instead).
def pack(xs, n):
    if n >= 0 and len(xs) > n : xs[n] = drop(xs, n)
    else : return None
    return xs

# SWITCH :: int -> int -> [int] -> [int]
# Given two integers n1 and n2, and one array xs, returns an array with the elements of index n1 and n2 in switched places.
def switch(xs, n1, n2):
    t = get(xs, n1)
    insert(xs, get(xs, n2), n1)
    insert(xs, t, n2)
    return xs

# MERGE :: list -> list -> int -> list
# Given lists xs1 and xs2, returns a new list with xs2 inserted into the n-th position of xs1
def merge(xs1, xs2, n):
    output = []
    for i in range(len(xs1)):
        if i == n - 1:
            output.append(xs2)
        output.append(xs1[i])
    return output

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
0: [to_string, 1, ['list'], 'str'],
1: [split, 1, ['str'], 'list'],
2: [take, 2, ['list', 'int'], 'list'],
3: [drop, 2, ['list', 'int'], 'list'],
4: [convert_data, 1, ['list'], 'list'],
5: [pack, 2, ['list', 'int'], 'list'],
6: [lowercase, 1, ['str'], 'str'],
#7: [merge, 3, ['list', 'list', 'int'], 'list']
#7: [switch, 3, ['list', 'int', 'int'], 'list'],
#8: [get, 2, ['list', 'int'], 'object'],
#9: [size, 1, ['list'], 'int'],
}

# TESTING
def test_methods():
    input = '10017 10209 1523779635 22.3 61 data3'
    print ('testing: ' + input)
    key = take(insert(convert_data(split(input)), drop(convert_data(split(input)), 3), 3), 3)
    print ('key : ' + str(key))
    # split
    a = method[1][0](input)
    print ('a : ' + str(a))
    # convert_data
    b = method[4][0](a)
    print ('b : ' + str(b))
    # pack
    d = method[5][0](b, 3)
    print ('d : ' + str(d))
    # take
    e = method[2][0](d, 3)
    # result
    print ('e (result) : ' + str(e))
    print ('Result == key : ' + str(e == key))
    return e

#test_methods()
