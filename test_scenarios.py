import test_data
import interoperability
import clustering
import clustering_dsl
import logic
from timeit import timeit
from timeit import default_timer as timer
from datetime import datetime as dt

### RUN TESTS

def test_interoperability():
    test_pairs = test_data.interop_test_pairs
    ql = interoperability

    for i in range(len(test_pairs)):
        print('Test[' + str(i + 1) + ']:')
        ql.train(test_pairs[i][0], test_pairs[i][1], 5000, ql.num_methods - 1)
        print()

    print('Testing programs:')
    print()
    for t in test_pairs:
        print('Input:')
        print('\t' + str(t[0]))

        program = ql.search(t[0])

        if program == None:
            print('Program failure\n')
            continue

        print('Result:')
        for r in ql.run(t[0]):
            print('\t' + str(r))
        print('Program(s) used:')
        print('\t' + str(program) + ', ' + str(len(program)) + ' program(s)')
        print('Time:')
        print('\t' + str("%.2f" % (ql.time_search(t[0], 5000) * 100000)) + 'us')
        print()

    print('Test search:')
    try:
        s_test = [
            ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/1', 1234, -1, 'property1', 'property2', {'payload 1':123, 'payload2':456}],
            {'command':'PUBLISH', 'mid':1234, 'qos':0, 'pos':0, 'to_process':-1, 'packet':
                ['PUBLISH', False, 1, False, -1, -1, 'test/gmqtt/1', 1234, ['Test payload', 'Payload 2']], 'info':['property1', 'property2', 'property3', 'property4']},
        ]
        for i in s_test:
            print()
            print('Input:')
            print('\t' + str(i))
            print('Result:')
            for r in ql.run(i):
                print('\t' + str(r))
            print('Program(s) used:')
            p = ql.search(i)
            print('\t' + str(p) + ', ' + str(len(p)) + ' program(s)')
            print('Time:')
            print('\t' + str("%.2f" % (ql.time_search(i, 5000) * 100000)) + 'us')
    except TypeError:
        print('No program found')

def test_clustering():
    test_agents = test_data.clustering_sensors
    test_contexts = test_data.clustering_contexts
    test_pairs = test_data.clustering_test_pairs
    clustering_dsl.sensor_agents = test_agents
    ql = clustering

    for i in range(len(test_pairs)):
        print('Test[' + str(i + 1) + ']:')
        ql.train(test_pairs[i][0], test_pairs[i][1], 5000, ql.num_methods - 1)
        print()

    print('Testing programs:')
    print()
    for t in test_pairs:
        print('Input:')
        print('\t' + str(t[0]))

        program = ql.search(t[0])

        if program == None:
            print('Program failure\n')
            continue

        print('Result:')
        for r in ql.run(t[0]):
            print('\t' + str(r))
        print('Program(s) used:')
        print('\t' + str(program) + ', ' + str(len(program)) + ' program(s)')
        print('Time:')
        print('\t' + str("%.2f" % (ql.time_search(t[0], 5000) * 100000)) + 'us')
        print()

#    print('Test search:')
#    try:
#        s_test = [
#            ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/1', 1234, -1, 'property1', 'property2', {'payload 1':123, 'payload2':456}],
#            {'command':'PUBLISH', 'mid':1234, 'qos':0, 'pos':0, 'to_process':-1, 'packet':
#                ['PUBLISH', False, 1, False, -1, -1, 'test/gmqtt/1', 1234, ['Test payload', 'Payload 2']], 'info':['property1', 'property2', 'property3', 'property4']},
#        ]
#        for i in s_test:
#            print()
#            print('Input:')
#            print('\t' + str(i))
#            print('Result:')
#            for r in ql.run(i):
#                print('\t' + str(r))
#            print('Program(s) used:')
#            p = ql.search(i)
#            print('\t' + str(p) + ', ' + str(len(p)) + ' program(s)')
#            print('Time:')
#            print('\t' + str("%.2f" % (ql.time_search(i, 5000) * 100000)) + 'us')
#    except TypeError:
#        print('No program found')

def test_logic():
    test_pairs = test_data.logic_test_pairs
    ql = logic
    for i in range(len(test_pairs)):
        print('Test[' + str(i + 1) + ']:')
        ql.train(test_pairs[i][0], test_pairs[i][1], 5000, ql.num_methods)
        print()

    print('Testing programs:')
    print()
    for t in test_data.logic_search_data:
        for k, v in  test_data.actuators.items():
            v = False
        print('Input:')
        print('\t' + str(t))
        print('\t' + str(test_data.actuators))

        program = ql.search(t)

        if program == None:
            print('\tProgram failure\n')
            continue

        print('Result:')
        for r in ql.run(t):
            print('\t' + str(r))
        print('Program(s) used:')
        for p in program:
            print('\t' + str(p) + ', ')
        print(str(len(program)) + ' program(s)')
        print('Time:')
        print('\t' + str("%.2f" % (ql.time_search(t, 5000) * 100000)) + 'us')
        print()

test_interoperability()
test_clustering()
test_logic()

###################################################################################################
