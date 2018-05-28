from datetime import datetime as dt

sensor_agents = {
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

test_contexts = {
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


actuators = {
    'heater' : False,
    'cooler' : False,
}

logic_sensors_s1 = {
    'phone' : {
        'pos' : 1000,
    },
    'temp' : {
        'living_room' : 17,
    }
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
