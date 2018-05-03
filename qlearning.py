import dsl
import numpy
from datetime import datetime
import editdistance # HAS TO BE INSTALLED SEPARATELY: pip3 install editdistance
import time
from timeit import default_timer as timer
from timeit import timeit

### SET UP GLOBAL VARIABLES
program_dictionary = {}
num_methods = len(dsl.method)
max_tries = 20

R = []
for i in range(num_methods):
    R.append([])
    for j in range(num_methods):
        if i != j and dsl.method[i][3] == dsl.method[j][2][0]: R[i].append(j)

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
    attribute_type = [*dsl.method[method][2]]
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
    return route(new_in, new_out)
###################################################################################################

### FIND ROUTE BETWEEN INPUT -> OUTPUT
def route(input, output):
    global state

    q_progress = Q.copy()
    state = [input]
    route = []
    last_action = 0
    while current_state() != output:
        try:
            next_step_index = numpy.where(Q[last_action] == numpy.max(q_progress[last_action]))[1]
        except IndexError:
            next_step_index = numpy.where(Q[last_action] == numpy.max(q_progress[last_action]))[0]

        if next_step_index.shape[0] > 1:
            next_step_index = int(numpy.random.choice(next_step_index, size = 1))
        else:
            next_step_index = int(next_step_index)

        state.append(dsl_method(next_step_index))
        route.append(next_step_index)

        for i in range(num_methods):
            q_progress[i][last_action] = 0
        q_progress[last_action,] = 0

        print(str(next_step_index) + '>>')
        last_action = next_step_index

        if len(route) > max_tries:
            return None

    print('Input:\n' + str(input))
    print('Selected path:\n' + str(route))
    print('Result:\n' + str(current_state()) + '\n')
    return [route, avg_time(route, 1000000)]
###################################################################################################

### RUN METHOD

def run(base, method):
    init(base, output)
    for m in method:
        state.append(dsl_method(m))
    return current_state

###################################################################################################

### TIME METHOD
avg_time = lambda method, iterations : timeit(run(input, method), number=iterations) / iterations
###################################################################################################

### KEY FROM INPUT
def comparison_key(input):
    key = [len(input)]
    for i in range(len(input)):
        if input[i] == " " : key.append(i)
    return key
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
        if find_types(program_dictionary[key)[0] == type(list): return program_dictionary[key][0]
        return program_dictionary[input]

    comparisons = sorted(reverse=True)#[]
    for k, p in program_dictionary.items():#sorted(program_dictionary):
        likeness = abs(key[0] - p[0]) + abs(len(key) - len(p))
        comparisons.append(likeness, p)

    print(comparisons)
    #input_likeness = editdistance.eval(str(io_pair[0]), str())
    #print(list_types(test_pairs[0][0]))
    #print(list_types(test_pairs[0][1]))
###################################################################################################

### RUN TESTS
test_pairs = [
    ['10017 10209 1523779635 22.3 61 data3', [10017, 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3']]],
    ['10017 10209 1523779635 22.3 61 data3 data4 17', [10017, 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3', 'data4', 17]]],
    ['10017 10209 22.3 61', [10017, 10209, 22.3, [61]]],
]

programs = []
for i in range(len(test_pairs)):
    print(comparison_key(test_pairs[i][0]))
    print('Test[' + str(i + 1) + ']:')

    try:
        program_dictionary[tuple(comparison_key(test_pairs[i][0]))] = tuple(train(test_pairs[i][0], test_pairs[i][1], 3000, 10))
    except TypeError: continue
    #programs.append(train(test_pairs[i][0], test_pairs[i][1], 3000, 10))

print('Testing programs:')
for t in test_pairs:
    print(t[0])
    key = tuple(comparison_key(t[0]))
    #if programs[t] is None :
    if key not in program_dictionary:
        print('Program failure\n')
        continue

    #print(str(programs[t][0]) + ', ' + str(len(programs[t][0])) + ' steps, ' + str("%.2f" % (programs[t][1] * 100000000)) + 'ns')
    print(str(program_dictionary[key][0]) + ', ' + str(len(program_dictionary[key][0])) + ' steps, ' + str("%.2f" % (program_dictionary[key][1] * 100000000)) + 'ns')

    run(t[0], program_dictionary[key][0])

    print(str(current_state()))
    print()
###################################################################################################
