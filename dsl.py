from datetime import datetime
from decimal import *
import re

# TOString :: Array -> Strings
# Given an array xs returns a string of said Array
to_string = lambda xs : str(xs)

# SPLIT :: String -> [String]
# Given a string, returns an array of strings divided by the blankspaces of the original string.
split = lambda s : s.split()

# TAKE :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array truncated after the (n+1)-st element.
# (If the length of xs was no larger than n in the first place, it is returned without modification.)
take = lambda xs, n : xs[:(n + 1)]

# DROP :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array with the first n elements dropped.
# (If the length of xs was no larger than n in the first place, an empty array is returned.)
drop = lambda xs, n : xs[n:]
#drop_char = lambda s : s[1:]
#drop_char_in_list = lambda xs : '[\'' + str(xs)[3:]

# CONVERT_DATA :: [String] -> Array
# Given an array of strings xs, returns an array of Strings, Integers, and or floats.
def convert_data(xs):
    type_format = [re.compile('.*=.*'), re.compile('.*:.*')]
    for i in range(len(xs)):
        e = xs[i]
        if isinstance(e, str):
            if e.isdigit():
                try:
                    if len(e) == 8:
                        xs[i] = datetime.strptime(e, '%Y%m%d')
                        continue
                    elif len(e) == 6:
                        xs[i] = datetime.strptime(e, '%y%m%d')
                        continue
                except ValueError: pass
                xs[i] = int(e)
                try:
                    d = datetime.fromtimestamp(xs[i])
                    dt = datetime.now()
                    if dt.year - d.year <= 1 and (dt.month - d.month <= 1 or dt.month - d.month == 11):
                        xs[i] = d
                except OSError: continue
            else:
                if type_format[0].match(e) is not None or type_format[1].match(e) is not None:
                    s = list(filter(None, re.split('=|\"|:', e)))
                    xs[i] = convert_data([s[0], s[1]])

                    continue
                try: xs[i] = float(e)
                except ValueError: continue
    return xs

# ADD_DATE :: List -> int -> list_types
# Given a list xs and integer i, returns xs with the current datetime added to the (i-1)-st positionself.
add_date = lambda xs, i: (xs, xs.insert(i - 1, datetime.now()))[0]

# INSERT :: int -> [object] ->[String] -> [String]
# Given an integer n, an object o or array, and an array xs, inserts s at the (n+1)-st position in xs, replacing the previous value if applicable
# and returns the new xs. (If the length of xs was less than or equal to n, the value NULL is returned instead).
def pack(xs, n):
    if n >= 0 and len(xs) > n : xs[n] = drop(xs, n)
    else : return None
    return xs

# DSL Method index
method = {
0: [to_string, ['list'], 'str'],
1: [split, ['str'], 'list'],
2: [take, ['list', 'int'], 'list'],
3: [drop, ['list', 'int'], 'list'],
4: [convert_data, ['list'], 'list'],
5: [pack, ['list', 'int'], 'list'],
}
