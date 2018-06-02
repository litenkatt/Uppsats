import csd_dsl
import test_data
import numpy
import editdistance # HAS TO BE INSTALLED SEPARATELY: pip3 install editdistance
from timeit import timeit
import copy

### SET UP GLOBAL VARIABLES
program_dictionary = {}
num_methods = len(csd_dsl.method)
max_tries = 20

R = []
for i in range(num_methods):
    R.append([])
    for j in range(num_methods):
        if i != num_methods - 1:
            if i != j and j != num_methods - 1 and (csd_dsl.method[i][2] == csd_dsl.method[j][1][0] or i == 0): R[i].append(j)
        else:
            R[i] = [0]

Q = numpy.zeros([num_methods, num_methods])
g = 0.8

input = ''
output = ''
state = [input]

def init(new_in, new_out):
    global input
    global output
    global state

    input = new_in.copy()
    state = [*new_in.copy()]
    output = new_out

current_state = lambda : state[len(state) - 1]
sample_action = lambda i : int(numpy.random.choice(R[i], 1))
###################################################################################################

### CALCULATE LIKENESS OF A RESULT AND THE OUTPUT EXAMPLE
compare = lambda r : editdistance.eval(str(r), str(output))
def score(result):
    if result == output : return 100
    if result is None : return -1
    types = [list_types(result), list_types(output)]
    s = 100 / (compare(result) + editdistance.eval(str(types[0]), str(types[1])) / (len(types[0]) + len(types[1])))
    if s < 0 : return 0
    return s
###################################################################################################

### RUN A SINGLE METHOD FROM THE DSL AND RETURN THE RESULT
def dsl_method(method):
    attribute_type = [*csd_dsl.method[method][1]]
    attributes = []

    for i in attribute_type:
        if len(attributes) == len(attribute_type) : break
        if i == 'dict' and len(attributes) > 0:
            attributes.append(state[0])
        else:
            for j in range(len(state) - 1, -1, -1):
                if str(type(state[j])) == '<class \'' + str(i) + '\'>' and state[j] not in attributes :
                    attributes.append(state[j])
                    break

    try:
        result = csd_dsl.method[method][0](*attributes)
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

    if qs == -1 : return -1
    Q[last_action, next_action] = qs + gamma * max_value
    return qs
###################################################################################################

#### TRAIN THE Q-TABLE
def train(new_in, new_out, iterations, max_steps):
    global Q
    global state
    init(new_in, new_out)

    for i in range(iterations):
        state = [*input]

        last_action = 0
        for j in range(max_steps):
                next_action = sample_action(last_action)
                if update(last_action, next_action, g) == -1: break
                #if next_action == num_methods - 1: break
                last_action = next_action

    Q = Q / numpy.max(Q) * 100

    for i in range(len(Q)):
        for j in range(len(Q)):
            Q[i][j] = format(Q[i][j], '.2f')#("%.2f" % Q[i][j])

    print("Trained Q matrix:")
    print(Q)

    rt = route(new_in, new_out)
    if rt != None:
        key = comparison_key(new_in[0])
        if key not in program_dictionary:
            program_dictionary[key] = [rt]
        else:
            if rt not in program_dictionary[key]:
                for i in range(len(program_dictionary[key])):
                    if len(rt) < len(program_dictionary[key][i]):
                        program_dictionary[key].insert(i, rt)
                        return rt
                program_dictionary[key].append(rt)
    return rt
###################################################################################################

### FIND ROUTE BETWEEN INPUT -> OUTPUT
def route(input, output):
    global state

    q_progress = Q.copy()
    state = [*input]
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

        if len(route) > max_tries or current_state() is None:
            return None

    if num_methods - 3 not in route:
        state.append(dsl_method(num_methods-3))
        route.append(num_methods-3)

    state.append(dsl_method(num_methods-1))
    route.append(num_methods-1)

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
    r = []
    for p in search(base):
        r.append(run_specific(base, p))
    #r.append(run_specific(base, search(base)[0]))
    return r

###################################################################################################

### TIME METHOD
time_run = lambda input, method, iterations : timeit(lambda: run_specific(input, method), number=iterations) / iterations
time_search = lambda input, iterations : timeit(lambda: run(input), number=iterations) / iterations
###################################################################################################

### KEY FROM INPUT
def comparison_key(input):
    #key = [0,[],[]]
    #print(input)
    #for sk, sv in input[0].items():
    #        for tk, tv in sv.items():
    #            key[0] += 1
    #            key[1].append(tk)

    #if result == None:
    #    for k, v in input[1].items():
    #        key[2].append(k)
    #else:
    #    for k, v in result.items():
    #        key[2].append(k)

    #print(key)
    #key[1] = tuple(key[1])
    #key[2] = tuple(key[2])
    #return tuple(key)

    key = [len(input)]
    for i in list_types(input):
        if(type(i) == 'list' or type(i) == 'dict'):
            key.append(comparison_key(i))
        else:
            key.append(i)

    return tuple(key)
###################################################################################################

### FIND PREVIOUS PROGRAM
list_types = lambda i : find_types(i) if isinstance(i, list) or isinstance(i, tuple) or isinstance(i, dict) else tuple([type(i)])
def find_types(list):
    r = []
    col = list.items() if isinstance(list, dict) else list
    for i in col:
        r.append(list_types(i))
    if len(r) > 1:
        return tuple(r)
    return r

def search(input):
    key = comparison_key(input[0])
    if key in program_dictionary:
        #print(program_dictionary[key])
        return program_dictionary[key]

    comparisons = []
    for k, li in program_dictionary.items():
        s = key if len(key) < len(k) else k
        matching_types = 0
        for i in range(len(s)):
            if key[i] == k[i]:
                matching_types += 1
        difference = abs(key[0] - k[0]) + abs(len(key) - len(k)) + len(key) - matching_types
        if isinstance(li[0], list):
            for p in li:
                if len(comparisons) < 1:
                    comparisons.append([difference, p, k])
                else:
                    for i in range(len(comparisons)):
                        if difference < comparisons[i][0]:
                            comparisons.insert(i, [difference, p, k])
                            break
        else:
            if len(comparisons) < 1:
                comparisons.append([difference, li, k])
            else:
                for i in range(len(comparisons)):
                    if difference < comparisons[i][0]:
                        comparisons.insert(i, [difference, li, k])
                        break


    for p in comparisons:
        if run_specific(input, p[1]) != None:
            return program_dictionary[p[2]]

    return None
###################################################################################################
