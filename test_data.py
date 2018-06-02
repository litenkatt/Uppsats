from datetime import datetime as dt

### INTEROPERABILITY

interop_test_pairs = [
    [   # 1: Eclipse Paho Python -> gmqtt
        {'command':'PUBLISH', 'mid':1234, 'qos':0, 'pos':0, 'to_process':9, 'packet':['PUBLISH', False, 0, False, 4, 30, 'test/gmqtt/eclipse_paho_python', 1234, 'Test data for learning'], 'info':'This message will be translated into gmqtt format'},
        ['PUBLISH', False, 0, False, 4, 30, 'test/gmqtt/eclipse_paho_python', 1234, [1, 'This message will be translated into gmqtt format', 'Test data for learning']]
    ],
    [   # 2: gmqtt -> Eclipse Paho Python
        ['PUBLISH', False, 1, False, 6, 30, 'test/eclipse_paho_python/gmqtt', 5678, 1, 'This message will be translated into Eclipse Paho Python format', 'Test data for learning'],
        {'command':'PUBLISH', 'mid':5678, 'qos':1, 'pos':0, 'to_process':9, 'packet':['PUBLISH', False, 1, False, 6, 30, 'test/eclipse_paho_python/gmqtt', 5678, 'Test data for learning'], 'info':[1, 'This message will be translated into Eclipse Paho Python format']}
    ],
]

interop_extra_pairs = [
    [   # gmqtt without mid-> MQTT Standard
        ['PUBLISH', False, 0, False, -1, -1, 'test/mqtt_standard/1', -1, 'property1', 'property2', 'Test payload'],
        ['PUBLISH', False, 0, False, -1, -1, 'test/mqtt_standard/1', [-1, 'property1', 'property2', 'Test payload']]
    ],
    [   # gmqtt with mid -> MQTT Standard
        ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/2', 1234, -1, 'property1', 'property2', 'Test payload'],
        ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/2', 1234, [-1, 'property1', 'property2', 'Test payload']]
    ],
    [   # Eclipse Paho Python -> MQTT Standard
        {'command':'PUBLISH', 'mid':1234, 'qos':0, 'pos':0, 'to_process':-1, 'packet':['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/3', 1234, 'Test payload'], 'info':'property1'},
        ['PUBLISH', False, 1, False, -1, -1, 'test/mqtt_standard/3', 1234, 'Test payload']
    ],
    [   # MQTT Standard -> Eclipse Paho Python
        ['PUBLISH', False, 1, False, -1, -1, 'test/eclipse_paho_python/1', 1234, 'Test payload'],
        {'command':'PUBLISH', 'mid':1234, 'qos':1, 'pos':0, 'to_process':9, 'packet':['PUBLISH', False, 1, False, -1, -1, 'test/eclipse_paho_python/1', 1234, 'Test payload'], 'info':''}
    ],
]

interop_search_data = [
    {'command':'PUBLISH', 'mid':9012, 'qos':0, 'pos':0, 'to_process':9, 'packet':
        ['PUBLISH', False, 1, False, 4, 11, 'test/paho/1', 9012, ['Payload part 1', 'Payload part 2']], 'info':['property1', 'property2', 'property3', 'property4']},
    ['PUBLISH', False, 1, False, 7, 12, 'test/gmqtt/1', 3456, 2, 'property1', 'property2', {'payload part 1':123, 'payload part 2':456}],
    ['Erroneous input']
]

###################################################################################################

### Context sensing diversity

csd_sensors = {
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
    },
    'sensor102' : {
        'temp' : 28.1,
        'time' : dt(2018, 5, 20, 10, 0, 0),
        'loc' : 'Kista'
    },
    'sensor103' : {
        'temp' : 28.1,
        'time' : dt(2018, 5, 20, 10, 0, 0),
        'loc' : 'Bromma'
    }
}

csd_contexts = {
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

csd_test_pairs = [
    [
        [
            {
                'sensor101' : {
                    'temp' : 26.4,
                    'time' : dt(2018, 5, 20, 10, 0, 0),
                    'loc' : 'Kista'
                }
            },
            csd_contexts
        ],
        {
            'c1' : [
                    'loc',
                    {
                        'loc' : [1, 0, 'Kista'],
                        'temp' : [1, 0, 20.3],
                        'time' : [1, 0, dt(2018, 5, 20, 0, 0, 0)],
                    },
                    ['sensor1',]
            ],
        }
    ],
    [
        [
            {
                'sensor101' : {
                    'temp' : 26.4,
                    'time' : dt(2018, 5, 20, 10, 0, 0),
                    'loc' : 'Kista'
                }
            },
            csd_contexts
        ],
        {
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
    ],
]

csd_search_data = [
    [
        {
            'sensor102' : {
                'temp' : 19.2,
                'time' : dt(2018, 5, 27, 10, 0, 0),
                'loc' : 'Kista'
            }
        },
        csd_contexts
    ],
    [
        {
            'sensor103' : {
                'temp' : 28.1,
                'time' : dt(2018, 5, 20, 10, 0, 0),
                'loc' : 'Bromma'
            }
        },
        csd_contexts
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

window_test_pair = [
    [
        [
            [
                [
                    'rain',
                    'window'
                ],
                0
            ],
            1,
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
                'windows' : True
        }
    ],
]

actuators = {
    'heater' : False,
    'cooler' : False,
    'windows' : False,
}

logic_search_data = [

    ### Scenario 1

    [
        [
            ['phone', 'pos'],
            2000
        ],
        [
            ['temp', 'living_room'],
            18
        ],
    ],
    [
        [
            ['phone', 'pos'],
            1200
        ],
        [
            ['temp', 'living_room'],
            16
        ],
    ],
    [
        [
            ['phone', 'pos'],
            0
        ],
        [
            ['temp', 'living_room'],
            25
        ],
    ],
]

bonus_scenarios = [

    ### Scenario 2

    [
        [
            ['phone', 'pos'],
            10000
        ],
        [
            ['temp', 'living_room'],
            16
        ],
    ],
    [
        [
            ['phone', 'pos'],
            5000
        ],
        [
            ['temp', 'living_room'],
            15
        ],
    ],
    [
        [
            ['phone', 'pos'],
            1000
        ],
        [
            ['temp', 'living_room'],
            15
        ],
    ],
    [
        [
            ['phone', 'pos'],
            500
        ],
        [
            ['temp', 'living_room'],
            21
        ],
    ],

    ### Scenario 3

    [
        [
            ['rain', 'window'],
            0
        ],
        [
            ['temp', 'living_room'],
            21
        ],
    ],
    [
        [
            ['rain', 'window'],
            1
        ],
        [
            ['temp', 'living_room'],
            24
        ],
    ],
    [
        [
            ['rain', 'window'],
            0
        ],
        [
            ['temp', 'living_room'],
            25
        ],
    ],
    [
        [
            ['rain', 'window'],
            0
        ],
        [
            ['temp', 'living_room'],
            19
        ],
    ],
]

###################################################################################################
