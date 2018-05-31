import test_data
import math
import editdistance
import copy
from datetime import datetime
from collections import Counter

sensor_agents = test_data.csd_sensors

# SORT :: [Sensor_agent] -> Integer -> [Sensor_agent]
# Given a list xc and int i returns xc sorted according to i
sort = lambda xc, i: xc.sort(key=lambda x: x[i])

# MEAN :: List -> Decimal
# Given a list xc returns a list of the mean values on axis 0
mean = lambda xc: np.mean(xc)

# STD :: List -> Decimal
# Given a list xc returns a list of the standard deviation values on axis 0
std = lambda xc: np.std(xc)

### ADDING TO CONTEXT

def add_sensor(context, sensor):
    xc = copy.deepcopy(context)
    for id, c in xc.items():
        cont = False

        for sa in sensor.keys():
            if sa in c[2]: continue
            c[2].append(sa)
            cont = True

        if cont == False: continue

        topics = {}
        for sa in c[2]:
            for t, v in sensor_agents[sa].items():
                if t in topics:
                    topics[t].append(v)
                else:
                    topics[t] = [v]

        for sk, sv in sensor.items():
            for t, v in sv.items():
                if t in c[1]:
                    n = c[1][t][0] + 1
                    std = c[1][t][1]
                    avg = c[1][t][2]

                    # Int, float
                    if isinstance(avg, int) or isinstance(avg, float):
                        avg = ((avg * (n - 1)) + v) / n

                        var = 0
                        for i in range(n):
                            var += (topics[t][i] - avg) * (topics[t][i] - avg)

                        std = math.sqrt(var / n)

                    # Datetime
                    elif isinstance(avg, datetime):
                        avg_y = int(round(((avg.year * (n - 1)) + v.year) / n))
                        avg_m = int(round(((avg.month * (n - 1)) + v.month) / n))
                        avg_d = int(round(((avg.day * (n - 1)) + v.day) / n))
                        avg_h = int(round(((avg.hour * (n - 1)) + v.hour) / n))
                        avg_mt = int(round(((avg.minute * (n - 1)) + v.minute) / n))
                        avg_s = int(round(((avg.second * (n - 1)) + v.second) / n))
                        avg = datetime(avg_y, avg_m, avg_d, avg_h, avg_mt, avg_s)

                        var = datetime_variance(avg, topics[t])

                        std = datetime_to_seconds(math.sqrt(var[0] / n), math.sqrt(var[1] / n), math.sqrt(var[2] / n),
                            math.sqrt(var[3] / n), math.sqrt(var[4] / n), math.sqrt(var[5] / n))

                    # String
                    else:
                        avg = Counter(topics[t]).most_common(1)[0][0]

                        var = 0
                        for i in range(n):
                            dist = editdistance.eval(str(topics[t][i]), avg)
                            var += (dist * dist)

                        std = math.sqrt(var / n)

                    # Update fields
                    c[1][t] = [n, std, avg]

                else:
                    c[1][t] = [1, 0, v]
    return xc

def datetime_variance(avg, v):
    var = [0, 0, 0, 0, 0, 0]
    for i in v:
        var[0] += (i.year - avg.year) ** 2
        var[1] += (i.month - avg.month) ** 2
        var[2] += (i.day - avg.day) ** 2
        var[3] += (i.hour - avg.hour) ** 2
        var[4] += (i.minute - avg.minute) ** 2
        var[5] += (i.second - avg.second) ** 2
    return var

datetime_convert = lambda dt : datetime_to_seconds(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
datetime_to_seconds = lambda y, m, d, h, mt, s : y * 60 * 60 * 24 * 365 + m * 60 * 60 * 24 * 30 + d * 60 * 60 * 24 + h * 60 * 60 + mt  * 60 + s
###################################################################################################

### EXCLUDE CONTEXTS WITH TOP-ELEMENT OF DATATYPE

def exclude_strings(xc):
    r = {}
    for k, v in xc.items():
        if not isinstance(v[1][v[0]][2], str):
            r[k] = v
    return r

def exclude_ints(xc):
    r = {}
    for k, v in xc.items():
        if not isinstance(v[1][v[0]][2], int):
            r[k] = v
    return r

def exclude_floats(xc):
    r = {}
    for k, v in xc.items():
        if not isinstance(v[1][v[0]][2], float):
            r[k] = v
    return r

def exclude_dates(xc):
    r = {}
    for k, v in xc.items():
        if not isinstance(v[1][v[0]][2], datetime):
            r[k] = v
    return r

def exclude_outside_std(xc, sensor):
    r = {}
    for ck, cv in xc.items():
        for sk, sa in sensor.items():
            t = cv[0]
            if t in sa:
                v = sa[t]
                avg = cv[1][t]

                if isinstance(v, int) or isinstance(v, float):
                    if v < (avg[2] - avg[1]) or (avg[2] + avg[1]) < v:
                        break

                elif isinstance(v, datetime):
                    s = datetime_convert(v)
                    avg_s = datetime_convert(avg[2])
                    if s < (avg_s - avg[1]) or (avg_s + avg[1]) < s:
                        break

                else:
                    if editdistance.eval(str(v), avg[2]) > avg[1]:
                        break

                r[ck] = cv
    return r

def exclude_outside_avg(xc, sensor):
    r = {}
    for ck, cv in xc.items():
        for sk, sa in sensor.items():
            t = cv[0]
            if t in sa:
                if sa[t] == cv[1][t][2]:
                    r[ck] = cv

    return r

###################################################################################################

start = lambda : None

### DSL METHOD INDEX
method = [
    [start, [None], None],
    [exclude_strings, ['dict'], 'dict'],
    [exclude_ints, ['dict'], 'dict'],
    [exclude_floats, ['dict'], 'dict'],
    [exclude_dates, ['dict'], 'dict'],
    [exclude_outside_std, ['dict', 'dict'], 'dict'],
    [exclude_outside_avg, ['dict', 'dict'], 'dict'],
    [add_sensor, ['dict', 'dict'], 'dict'],
]
###################################################################################################


### TEST

se = {
    'sensor101' : {
        'temp' : 26.4,
        'time' : datetime(2018, 5, 20, 10),
        'loc' : 'Kista'
    }
}

test_contexts = {
    'c1' : [
            'loc',
            {
                'loc' : [1, 0, 'Kista'],
                'temp' : [1, 0, 20.3],
                'time' : [1, 0, datetime(2018, 5, 20, 0, 0, 0)],
            },
            ['sensor1',]
    ],
    'c2' : [
            'loc',
            {
                'loc' : [1, 0, 'Solna'],
                'temp' : [1, 0, 21.2],
                'time' : [1, 0, datetime(2018, 5, 20, 0, 0, 0)],
            },
            ['sensor2',]
    ],
    'c3' : [
            'time',
            {
                'loc' : [2, 2.82842712, 'Kista'],
                'time' : [2, 0, datetime(2018, 5, 20, 10, 0, 0)],
                'temp' : [2, 0.31819805, 20,75],
            },
            ['sensor1', 'sensor2']
    ],
}

#print(add_sensor({'c1' : test_contexts['c1']}, se))
#print(add_sensor({'c3' : test_contexts['c3']}, se))
#print()
#for k, v in exclude_outside_std(scenarios.test_contexts, se).items(): print(str(k) + ' : ' + str(v))
#print(exclude_strings(test_contexts))
