import logical_dsl as dsl
import numpy
from datetime import datetime
import editdistance # HAS TO BE INSTALLED SEPARATELY: pip3 install editdistance
import time
from timeit import default_timer as timer
from timeit import timeit

### SET UP GLOBAL VARIABLES
program_dictionary = {}
num_methods = len(dsl.method)

R = []
for i in range(num_methods):
    R.append([])
    for j in range(num_methods):
        if i != j and dsl.method[i][2] == dsl.method[j][1][0]: R[i].append(j)

Q = numpy.zeros([num_methods, num_methods])
g = 0.8

input = '10017 10209 1523779635 22.3 61 data3'
output = [10017, 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3']]
state = [input]

def init(new_in, new_out):
    global input
    global output
    global state

    input = new_in
    state = [input]
    output = new_out

current_state = lambda : state[len(state) - 1]
sample_action = lambda i : int(numpy.random.choice(R[i], 1))
###################################################################################################

### CALCULATE LIKENESS OF A RESULT AND THE OUTPUT EXAMPLE
compare = lambda r : 100 - editdistance.eval(str(r), str(output))
def score(result):
    if result == output : return 100
    if result is None : return -1
    s = compare(result)
    if s < 0 : return 0
    return compare(result)
###################################################################################################

### RUN A SINGLE METHOD FROM THE DSL AND RETURN THE RESULT
def dsl_method(method):
    attribute_type = [*dsl.method[method][1]]
    attributes = []

    for i in attribute_type:
        if len(attributes) > len(attribute_type) : break
        if i == 'int':
            attributes.append(3)
            continue

        for j in range(len(state) - 1, -1, -1):
            if str(type(state[j])) == '<class \'' + str(i) + '\'>' and state[j] not in attributes : attributes.append(state[j])

    try:
        result = dsl.method[method][0](*attributes)
        state.append(result)
        return result
    except TypeError:
        return None
###################################################################################################

### RUN NEXT ACTION AND UPDATE THE CORRESPONDING Q-VALUE IN THE Q-TABLE
def update(last_action, next_action, gamma):
    max_index = numpy.where(Q[next_action] == numpy.max(Q[next_action]))[0]

    if max_index.shape[0] > 1:
        max_index = int(numpy.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)

    max_value = Q[next_action, max_index]

    qs = score(dsl_method(next_action))
    if qs == -1 : return
    Q[last_action, next_action] = qs + gamma * max_value
###################################################################################################

#### TRAIN THE Q-TABLE
def learn(iterations, max_tries):
    global state

    for i in range(iterations):
        state = [input]
        last_action = 0

        for j in range(max_tries):
            next_action = sample_action(last_action)
            update(last_action, next_action, g)
            last_action = next_action

def train(new_in, new_out, iterations, max_steps):
    global Q
    init(new_in, new_out)

    learn(iterations, max_steps)
    Q = Q / numpy.max(Q) * 100

    for i in range(len(Q)):
        for j in range(len(Q)):
            Q[i][j] = "%.2f" % Q[i][j]

    print("Trained Q matrix:")
    print(Q)

    rt = route(new_in, new_out, max_steps)
    if rt != None:
        key = comparison_key(new_in)
        if key not in program_dictionary:
            program_dictionary[key] = [rt]
        else:
            if rt not in program_dictionary[key]:
                for i in range(len(program_dictionary[key])):
                    if len(rt) < len(program_dictionary[key][i]):
                        program_dictionary[key].insert(i, rt)

    return rt
###################################################################################################

### FIND ROUTE BETWEEN INPUT -> OUTPUT
def route(input, output, max_tries):
    global state

    q_progress = Q.copy()
    state = [input]
    route = []
    last_action = 0
    while current_state() != output:
        try:
            next_step_index = numpy.where(q_progress[last_action] == numpy.max(q_progress[last_action]))[1]
        except IndexError:
            next_step_index = numpy.where(q_progress[last_action] == numpy.max(q_progress[last_action]))[0]

        if next_step_index.shape[0] > 1:
            next_step_index = int(numpy.random.choice(next_step_index, size = 1))
        else:
            next_step_index = int(next_step_index)

        state.append(dsl_method(next_step_index))
        route.append(next_step_index)

        for i in range(num_methods):
            q_progress[i][last_action] = 0
        q_progress[last_action,] = 0
        last_action = next_step_index

        if len(route) > max_tries:
            return None

    print('Input:\n' + str(input))
    print('Selected path:\n' + str(route))
    print('Result:\n' + str(current_state()) + '\n')
    return route
###################################################################################################

### RUN METHOD
def run_specific(base, method):
    init(base, None)
    for m in method:
        state.append(dsl_method(m))
    return current_state()

def run(base):
    return run_specific(base, search(base))

###################################################################################################

### TIME METHOD
time_run = lambda input, method, iterations : timeit(lambda: run_specific(input, method), number=iterations) / iterations
time_search = lambda input, iterations : timeit(lambda: run(input), number=iterations) / iterations
###################################################################################################

### KEY FROM INPUT
def comparison_key(input):
    key = [len(input)]
    for i in range(len(input)):
        if input[i] == " " : key.append(i)
    return tuple(key)
###################################################################################################

### FIND PREVIOUS PROGRAM
list_types = lambda i : find_types(i) if isinstance(i, list) else type(i)
def find_types(list):
    r = []
    for i in list:
        r.append(list_types(i))
    return r

def search(input):
    key = comparison_key(input)
    if key in program_dictionary:
        return program_dictionary[key][0]

    comparisons = []
    for k, li in program_dictionary.items():
        if isinstance(li[0], list):
            for p in li:
                difference = abs(key[0] - k[0]) + abs(len(key) - len(k)) + len(key) - len(set(key).intersection(k))
                if len(comparisons) < 1:
                    comparisons.append([difference, p])
                else:
                    for i in range(len(comparisons)):
                        if difference < comparisons[i][0]:
                            comparisons.insert(i, [difference, p])
                            break
        else:
            difference = abs(key[0] - k[0]) + abs(len(key) - len(k)) + len(key) - len(set(key).intersection(k))
            if len(comparisons) < 1:
                comparisons.append([difference, li])
            else:
                for i in range(len(comparisons)):
                    if difference < comparisons[i][0]:
                        comparisons.insert(i, [difference, li])
                        break

    for p in comparisons:
        if run_specific(t[0], p[1]) != None:
            return p[1]

    return None
###################################################################################################

### RUN TESTS
test_pairs = [
    ['10017 10209 1523779635 22.3 61 data3', [10017, 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3']]],
    #['10017 10209 1523779635 22.3 61 data3 data4 17', [10017, 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3', 'data4', 17]]],
    #['10017 10209 22.3 61', [10017, 10209, 22.3, [61]]],
    #['#10017 10209 1523779635 22.3 61 data3', ['#10017', 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3']]],
    #['id="10017" node_id="10209" datetime="1523779635" temp="22.3" humidity="61" label="data3"', [['id', 10017], ['node_id', 10209], ['datetime', datetime(2018, 4, 15, 10, 7, 15)], [['temp', 22.3], ['humidity', 61], ['label', 'data3']]]],
]

for i in range(len(test_pairs)):
    print('Test[' + str(i + 1) + ']:')
    train(test_pairs[i][0], test_pairs[i][1], 10000, num_methods)

print()
print('Testing programs:')
for t in test_pairs:
    print('Input:')
    print(t[0])

    program = search(t[0])

    if program == None:
        print('Program failure\n')
        continue

    print('Output:')
    print(run(t[0]))

    print('Program used:')
    print(str(program) + ', ' + str(len(program)) + ' steps')
    print('Time:')
    print(str("%.2f" % (time_search(t[0], 10000) * 30000)) + 'us')
    print()

print(program_dictionary)
try:
    print(run('10017 10209 1523779635 22.3 612 data3 data4'))
    print(search('10017 10209 1523779635 22.3 612 data3 data4'))
    print(str("%.2f" % (time_search(t[0], 10000) * 100000)) + 'us')
except TypeError:
    print('No program found')
###################################################################################################
