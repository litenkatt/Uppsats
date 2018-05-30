from datetime import datetime as dt

### INTEROPERABILITY

interop_test_pairs = [
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

clustering_sensors = {
    'sensor1' : {
        'temp' : 20.3,
        'time' : dt(2018, 5, 20, 10, 0, 0),
        'loc' : 'Kista'
    },
    'sensor2' : {
        'temp' : 21.2,
        'time' : dt(2018, 5, 20, 10, 0, 0),
        'loc' : 'Solna'
    },
    'sensor101' : {
        'temp' : 26.4,
        'time' : dt(2018, 5, 20, 10, 0, 0),
        'loc' : 'Kista'
    }
}

clustering_contexts = {
    'c1' : [
            'loc',
            {
                'loc' : [1, 0, 'Kista'],
                'temp' : [1, 0, 20.3],
                'time' : [1, 0, dt(2018, 5, 20, 0, 0, 0)],
            },
            ['sensor1',]
    ],
    'c2' : [
            'loc',
            {
                'loc' : [1, 0, 'Solna'],
                'temp' : [1, 0, 21.2],
                'time' : [1, 0, dt(2018, 5, 20, 0, 0, 0)],
            },
            ['sensor2',]
    ],
    'c3' : [
            'time',
            {
                'loc' : [2, 2.82842712, 'Kista'],
                'time' : [2, 0, dt(2018, 5, 20, 10, 0, 0)],
                'temp' : [2, 0.31819805, 20,75],
            },
            ['sensor1', 'sensor2']
    ],
}

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
            clustering_contexts
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

logic_test_pairs = [
    [
        [
            [
                [
                    'phone',
                    'pos'
                ],
                1000
            ],
            0,
            [
                [
                    'temp',
                    'living_room'
                ],
                17
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
                1000
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

actuators = {
    'heater' : False,
    'cooler' : False,
}

logic_search_data = [
    [
        [
            ['phone', 'pos'],
            1000
        ],
        [
            ['temp', 'living_room'],
            17
        ],
    ],
    [
        [
            ['phone', 'pos'],
            1000
        ],
        [
            ['temp', 'living_room'],
            20
        ],
    ],
    [
        [
            ['phone', 'pos'],
            1500
        ],
        [
            ['temp', 'living_room'],
            17
        ],
    ],
    [
        [
            ['phone', 'pos'],
            1200
        ],
        [
            ['temp', 'living_room'],
            14
        ],
    ],
]

###################################################################################################
