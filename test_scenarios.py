import test_data
import qlearning
import clustering_qlearning
import clustering_dsl
import logic_qlearning
from timeit import timeit
from timeit import default_timer as timer
from datetime import datetime as dt

### INSTANTIATION/INTEROPERABILITY

test_pairs = [
    [   # 1: gmqtt without mid-> MQTT Standard
        ['PUBLISH', False, 0, False, -1, -1, 'test/mqtt_standard/1', -1, 'property1', 'property2', 'Test payload'],
        ['PUBLISH', False, 0, False, -1, -1, 'test/mqtt_standard/1', [-1, 'property1', 'property2', 'Test payload']]
    ],
    [   # 2: gmqtt with mid -> MQTT Standard
        ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/2', 1234, -1, 'property1', 'property2', 'Test payload'],
        ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/2', 1234, [-1, 'property1', 'property2', 'Test payload']]
    ],
    [   # 3: Eclipse Paho Python -> MQTT Standard
        {'command':'PUBLISH', 'mid':1234, 'qos':0, 'pos':0, 'to_process':-1, 'packet':['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/3', 1234, 'Test payload'], 'info':'property1'},
        ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/3', 1234, 'Test payload']
    ],
    [   # 4: Eclipse Paho Python -> gmqtt
        {'command':'PUBLISH', 'mid':1234, 'qos':0, 'pos':0, 'to_process':-1, 'packet':['PUBLISH', False, 1, False, -1, -1, 'test/gmqtt/1', 1234, 'Test payload'], 'info':'property1'},
        ['PUBLISH', False, 1, False, -1, -1, 'test/gmqtt/1', 1234, [-1, 'property1', 'Test payload']]
    ],
    [   # 5: MQTT Standard -> Eclipse Paho Python
        ['PUBLISH', False, 1, False, -1, -1, 'test/eclipse_paho_python/1', 1234, 'Test payload'],
        {'command':'PUBLISH', 'mid':1234, 'qos':1, 'pos':0, 'to_process':9, 'packet':['PUBLISH', False, 1, False, -1, -1, 'test/eclipse_paho_python/1', 1234, 'Test payload'], 'info':''}
    ],
    [   # 6: gmqtt -> Eclipse Paho Python
        ['PUBLISH', False, 1, False, -1, -1, 'test/eclipse_paho_python/1', 1234, -1, 'property1', 'Test payload'],
        {'command':'PUBLISH', 'mid':1234, 'qos':1, 'pos':0, 'to_process':9, 'packet':['PUBLISH', False, 1, False, -1, -1, 'test/eclipse_paho_python/1', 1234, 'Test payload'], 'info':[-1, 'property1']}
    ],
]

###################################################################################################

### Clustering

test_agents = test_data.sensor_agents
test_contexts = test_data.test_contexts

clustering_test_pairs = [
    [
        [
            {
                'sensor101' : {
                    'temp' : 26.4,
                    'time' : dt(2018, 5, 20, 10, 0, 0),
                    'loc' : 'Kista'
                }
            },
            test_contexts
        ],
        {
            'c1': [
                'loc',
                {
                    'loc': [2, 0.0, 'Kista'],
                    'temp': [2, 3.049999999999999, 23.35],
                    'time': [2, 18000.0, dt(2018, 5, 20, 5, 0)]
                },
                ['sensor1', 'sensor101']
            ],
            'c3': [
                'time',
                {
                    'loc': [3, 2.309401076758503, 'Kista'],
                    'temp': [3, 2.734755727462488, 22.133333333333336],
                    'time': [3, 0.0, dt(2018, 5, 20, 10, 0)],
                },
                ['sensor1', 'sensor2', 'sensor101']
            ],
        }
    ],
]

###################################################################################################

### LOGIC

ls_1 = test_data.logic_sensors_s1

logic_test_pairs = [
    [
        [
            [
                [
                    'phone',
                    'pos'
                ],
                ls_1['phone']['pos']
            ],
            0,
            [
                [
                    'temp',
                    'living_room'
                ],
                ls_1['temp']['living_room']
            ],
            21
        ],
        {
                'heater' : True
        }
    ],
    [
        [
            [
                [
                    'phone',
                    'pos'
                ],
                ls_1['phone']['pos']
            ],
            0,
            [
                [
                    'temp',
                    'living_room'
                ],
                25
            ],
            21
        ],
        {
                'cooler' : True
        }
    ],
]



###################################################################################################

### RUN TESTS

def test_interoperability():
    ql = qlearning
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
    clustering_dsl.sensor_agents = test_agents
    ql = clustering_qlearning
    for i in range(len(clustering_test_pairs)):
        print('Test[' + str(i + 1) + ']:')
        ql.train(clustering_test_pairs[i][0], clustering_test_pairs[i][1], 5000, ql.num_methods - 1)
        print()

    print('Testing programs:')
    print()
    for t in clustering_test_pairs:
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
    ql = logic_qlearning
    for i in range(len(logic_test_pairs)):
        print('Test[' + str(i + 1) + ']:')
        ql.train(logic_test_pairs[i][0], logic_test_pairs[i][1], 5000, ql.num_methods)
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

#test_interoperability()
#test_clustering()
test_logic()

###################################################################################################
