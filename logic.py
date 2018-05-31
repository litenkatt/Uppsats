import logic_dsl
import test_data
import numpy
import editdistance # HAS TO BE INSTALLED SEPARATELY: pip3 install editdistance
from timeit import timeit
import copy
import operator
import math

### SET UP GLOBAL VARIABLES
actuator_keys = []
program_dictionary = {}
num_methods = len(test_data.actuators)
max_tries = 20

o = {
    '<': operator.lt,
    '>': operator.gt,
}



Q = numpy.zeros([num_methods * 2, num_methods * 2])
g = 0.8

input = []
output = {}
state = {}

def new_actuator(id, mode, counter):
    R.append([])
    actuator_keys.append([mode, id])
    for j in range(num_methods * 2):
        if counter != j: R[counter].append(j)

R = []
c = 0
for a in test_data.actuators:
    new_actuator(a, 0, c)
    c += 1
    new_actuator(a, 1, c)
    c += 1

def init(new_in, new_out):
    global input
    global output
    global state

    input = new_in.copy()
    state = {}
    output = new_out

sample_action = lambda i : int(numpy.random.choice(R[i], 1))
###################################################################################################

### CALCULATE LIKENESS OF A RESULT AND THE OUTPUT EXAMPLE
def score(result):
    if result == output : return 100
    if result is None : return -1

    s = 0
    for k, v in output.items():
        if k in state:
            if state[k] == v:
                s += 1
    s = 100 * (s / len(output))
    return s
###################################################################################################

### RUN A SINGLE METHOD FROM THE DSL AND RETURN THE RESULT
def dsl_method(method):
    attributes = actuator_keys[method]
    attribute_type = [*logic_dsl.method[attributes[0]][1]]
    try:
        result = logic_dsl.method[attributes[0]][0](attributes[1])
        state[result[0]] = result[1]
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

    if qs == -1 : return -1
    Q[last_action, next_action] = qs + gamma * max_value
    return qs
###################################################################################################

#### TRAIN THE Q-TABLE

def build_prog(rt, new_in):
    p = [rt]
    p.append(abs((new_in[3] - new_in[2][1]) / (new_in[1] - new_in[0][1])))
    if new_in[1] - new_in[0][1] > 0:
        p.append([new_in[0][1], '<'])
    else:
        p.append([new_in[0][1], '>'])

    if new_in[3] - new_in[2][1] > 0:
        p.append([new_in[3], '<'])
    else:
        p.append([new_in[3], '>'])

    return p

def train(new_in, new_out, iterations, max_steps):
    global Q
    global state
    init(new_in, new_out)
    m = abs((new_in[3] - new_in[2][1]) / (new_in[1] - new_in[0][1]))

    for i in range(iterations):
        state = {}

        last_action = numpy.random.randint(0, len(actuator_keys))

        for j in range(max_steps):
                next_action = sample_action(last_action)

                if update(last_action, next_action, g) == -1: break
                last_action = next_action

    Q = Q / numpy.max(Q) * 100

    for i in range(len(Q)):
        for j in range(len(Q)):
            Q[i][j] = "%.2f" % Q[i][j]

    print("Trained Q matrix:")
    print(Q)

    rt = route(new_in, new_out)
    if rt != None:
        rt = build_prog(rt, new_in)

        key = comparison_key([new_in[0], new_in[2]])

        if key not in program_dictionary:
            program_dictionary[key] = [rt]
        else:
            if rt not in program_dictionary[key]:
                program_dictionary[key].append(rt)

    for p in range(len(actuator_keys)):
        if p % 2 == 0:
            dsl_method(p)
    return rt
###################################################################################################

### FIND ROUTE BETWEEN INPUT -> OUTPUT
def route(input, output):
    global state

    q_progress = Q.copy()
    state = {}
    route = []
    last_action = 0
    while state != output:
        try:
            next_step_index = numpy.where(q_progress[last_action] == numpy.max(q_progress[last_action]))[1]
        except IndexError:
            next_step_index = numpy.where(q_progress[last_action] == numpy.max(q_progress[last_action]))[0]

        if next_step_index.shape[0] > 1:
            next_step_index = int(numpy.random.choice(next_step_index, size = 1))
        else:
            next_step_index = int(next_step_index)

        result = dsl_method(next_step_index)
        state[result[0]] = result[1]
        route.append(next_step_index)

        for i in range(num_methods):
            q_progress[i][last_action] = 0
        q_progress[last_action,] = 0
        last_action = next_step_index

        if len(route) > max_tries or result is None:
            return None

    print('Input:\n' + str(input))
    print('Selected path:\n' + str(route))
    print('Result:\n' + str(state) + '\n')
    return route
###################################################################################################

### RUN METHOD
def run_specific(i, method):
    init(i, None)
    if o[method[3][1]](i[1][1], method[3][0]):
        try:
            if abs((method[3][0] - i[1][1]) / (i[0][1])) >= method[1]:
                for m in method[0]:
                    result = dsl_method(m)
                    state[result[0]] = result[1]
                return state

        except ZeroDivisionError:
            if abs((method[3][0] - i[1][1]) / (1 + i[0][1])) >= method[1]:
                for m in method[0]:
                    result = dsl_method(m)
                    state[result[0]] = result[1]
                return state

    for m in method[0]:
        if m % 2 == 0:
            result = dsl_method(m + 1)
        else:
            result = dsl_method(m - 1)

        state[result[0]] = result[1]

    return state

def run(i):
    r = []
    for p in search(i):
        r.append(run_specific(i, p))

    return r

###################################################################################################

### TIME METHOD
time_run = lambda input, method, iterations : timeit(lambda: run_specific(input, method), number=iterations) / iterations
time_search = lambda input, iterations : timeit(lambda: run(input), number=iterations) / iterations
###################################################################################################

### KEY FROM INPUT
def comparison_key(input):
    return tuple([tuple(input[0][0]), tuple(input[1][0])])
###################################################################################################

### FIND PREVIOUS PROGRAM

def search(input):
    key = comparison_key(input)
    if key in program_dictionary:
        return program_dictionary[key]

    return None
###################################################################################################
