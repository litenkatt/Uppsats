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
get = lambda n, xs : xs[n] if n>=0 and len(xs)>n else None

# TAKE :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array truncated after the n-th element.
# (If the length of xs was no larger than n in the first place, it is returned without modification.)
take = lambda n, xs : xs[:n]

# DROP :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array with the first n elements dropped.
# (If the length of xs was no larger than n in the first place, an empty array is returned.)
drop = lambda n, xs : xs[n:]

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
                except OSError: continue # print ("convert error at: " + str(i) + ", " + str(e))
            else:
                try: xs[i] = float(e)
                except ValueError: continue
    return xs

# INSERT :: int -> [object] ->[String] -> [String]
# Given an integer n, an object o or array, and an array xs, inserts s at the (n+1)-st position in xs, replacing the previous value if applicable
# and returns the new xs. (If the length of xs was less than or equal to n, the value NULL is returned instead).
def insert(o, n, xs):
    if n >= 0 and len(xs) > n : xs[n] = o
    else : return None
    return xs

# SWITCH :: int -> int -> [int] -> [int]
# Given two integers n1 and n2, and one array xs, returns an array with the elements of index n1 and n2 in switched places.
def switch(n1, n2, xs):
    t = get(n1, xs)
    insert(ACCESS(n2, xs), n1, xs)
    insert(t, n2, xs)
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
0: to_string,
1: split,
2: size,
3: lowercase,
4: get,
5: take,
6: drop,
7: convert_data,
8: insert,
9: switch,
}

# TESTING

input = '00017 00209 1523779635 22.3 61 data3'
print ('testing: ' + input)
key = take(4, insert(drop(3, convert_data(split(input))), 3, convert_data(split(input))))
print ('key: ' + str(key))
# print (method[5](4, method[8](method[6](3, method[7](method[1](input))), 3, method[7](method[1](input)))))

print ('\n')

# split
a = method[1](input)
print ('a: ' + str(a))
# convert_data
b = method[7](a)
print ('b: ' + str(b))
# drop
c = method[6](3, b)
print ('c: ' + str(c))
# insert
d = method[8](c, 3, b)
print ('d: ' + str(d))
# take
e = method[5](4, d)
# result
print ('e (result): ' + str(e) + '\n')
print ('Correct!' if e == key else 'Incorrect!')
