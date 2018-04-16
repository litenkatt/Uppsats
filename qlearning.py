import numpy
import dsl
from datetime import datetime

input = '10017 10209 1523779635 22.3 61 data3'
output = [10017, 10209, datetime(2018, 4, 15, 10, 7, 15), [22.3, 61, 'data3']]

num_methods = len(dsl.method)
Q = numpy.zeros([num_methods, num_methods])
g = 0.8
state = [input]

last_action = 0
sample_action = lambda : int(numpy.random.choice(range(num_methods), 1))
next_action = sample_action()

def score(result):
    if result == output : return 100
    #if 


print (score(dsl.test_methods()))

def update(current_state, action, gamma):
    max_index = numpy.where(Q[action] == numpy.max(Q[action]))[0]

    if max_index.shape[0] > 1 : max_index = int(numpy.random.choice(max_index, size = 1))
    else : max_index = int(max_index)

    score = 1

    max_value = Q[action, max_index]
    Q[current_state, action] = score + gamma * max_value

update(last_action, next_action, g)

iterations = 10000
for i in range(iterations):
    last_action = numpy.random.randint(0, int(Q.shape[0]))
    action = sample_action()
    update(last_action, action, g)

print("Trained Q matrix:")
print(Q/numpy.max(Q)*100)
