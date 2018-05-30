# MQTT convert
mqtt_packet = ['command', 'dup', 'qos', 'retain', 'remaining_length', 'topic_length', 'topic', 'mid', 'payload']
epp_labels = ['command', 'mid', 'qos', 'pos', 'to_process', 'packet', 'info']
epp_keys = [['command', 'qos', 'mid'], ['pos', 'to_process', 'packet', 'info']]

# TAKE :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array truncated after the (n+1)-st element.
# (If the length of xs was no larger than n in the first place, it is returned without modification.)
take = lambda xs, n : xs[:n + 1]

# DROP :: int -> [String] -> [String]
# Given an integer n and array xs, returns the array with the first n elements dropped.
# (If the length of xs was no larger than n in the first place, an empty array is returned.)
drop = lambda xs, n : xs[n:]

def pack_payload(packet):
    p = packet.copy()
    mid = True if p[2] > 0 else False
    if len(p) > len(mqtt_packet) - 1 + mid:
        dif = len(mqtt_packet) - len(p) - 2 + mid
        if len(p) > abs(dif):
            p[dif] = drop(p, dif)
            return take(p, dif)
    return None

def label_packet(packet):
    p = packet.copy()
    dict = {
        'command':p[0],
        'qos':p[2],
        'pos':0,
    }
    mid = True if p[2] > 0 else False
    if mid: dict['mid'] = p[7]
    else: dict['mid'] = ''

    if len(p) > len(mqtt_packet) - 1 + mid:
        dif = len(mqtt_packet) - len(p) - 2 + mid
        if len(p) > abs(dif):
            dict['info'] = drop(p, dif)[:-1]
            dict['packet'] = p[:dif]
            dict['packet'].append(p[-1])
            dict['to_process'] = len(p) + dif + 1
    else:
        dict['info'] = ''
        dict['packet'] = p
        dict['to_process'] = len(p)

    return dict

def extract_packet(dict):
    if 'packet' in dict:
        return dict['packet']

    for k, v in dict:
        if type(v) == 'list' and len(v) >= len(mqtt_packet) - 1:
            return v
    return None

def pack_properties(packet, dict):
    p = packet.copy()
    if 'info' in dict:
        p[-1] = [-1, dict['info'], p[-1]]
        return p
    return None

start = lambda : None

# DSL Method index
method = [
    [start, [None], None],
    [pack_payload, ['list'], 'list'],
    [extract_packet, ['dict'], 'list'],
    [pack_properties, ['list', 'dict'], 'list'],
    [label_packet, ['list'], 'dict']
]
