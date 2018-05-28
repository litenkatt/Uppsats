import test_data

actuators = test_data.actuators

### Turning actuators ON/OFF

def on(act_id):
    actuators[act_id] = True
    return [act_id, True]

def off(act_id):
    actuators[act_id] = False
    return [act_id, False]

###################################################################################################

### DSL METHOD INDEX
method = [
    [off, ['str'], ['str', 'bool']],   
    [on, ['str'], ['str', 'bool']],
]
###################################################################################################
