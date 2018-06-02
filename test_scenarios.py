import test_data
import interoperability
import context_sensing_diversity
import logic
from timeit import timeit
from datetime import datetime as dt

### RUN TESTS

def test_interoperability():
    print('Testing Interoperability Module')
    print()
    test_pairs = test_data.interop_test_pairs
    ql = interoperability

    for i in range(len(test_pairs)):
        print('Rule[' + str(i + 1) + ']:')
        print('Time:\n\t' + str("%.2f" % ((timeit(lambda: ql.train(test_pairs[i][0], test_pairs[i][1], 5000, ql.num_methods - 1), number=1) / 1)  * 100000)) + 'us')
        print()

    print('Testing programs:')
    print()
    c = 1
    for t in test_data.interop_search_data:
        print('Test[' + str(c) + ']')
        c += 1

        print('Input:')
        print('\t' + str(t))

        program = ql.search(t)

        if program == None:
            print('\tProgram failure\n')
            continue
        print('Result:')
        for r in ql.run(t):
            print('\t' + str(r))

        print('Program(s) used:')
        try:
            for p in program:
                print('\t' + str(p) + ', ')
        except TypeError:
            print('\tNo programs found for \'' + str(t) + '\'...')

        print('Time:')
        print('\t' + str("%.2f" % (ql.time_search(t, 10000) * 100000)) + 'us')

        print()

def test_csd():
    print('Testing Context Sensing Diversity Module')
    print()
    test_pairs = test_data.csd_test_pairs
    ql = context_sensing_diversity

    for i in range(len(test_pairs)):
        print('Rule[' + str(i + 1) + ']:')
        print('Time:\n\t' + str("%.2f" % ((timeit(lambda: ql.train(test_pairs[i][0], test_pairs[i][1], 5000, ql.num_methods - 1), number=1) / 1)  * 100000)) + 'us')
        print()

    print('Testing programs:')
    print()
    c = 1
    for t in test_data.csd_search_data:
        print('Test[' + str(c) + ']')
        c += 1

        print('Input:')
        print('\t' + str(t))

        program = ql.search(t)

        if program == None:
            print('\tProgram failure\n')
            continue

        print('Result:')
        for r in ql.run(t):
            print('\t' + str(r))
        print('Program(s) used:')
        try:
            for p in program:
                print('\t' + str(p) + ', ')
        except TypeError:
            print('\tNo programs found for \'' + str(t) + '\'...')
        print('Time:')
        print('\t' + str("%.2f" % (ql.time_search(t, 5000) * 100000)) + 'us')
        print()

def test_logic():
    print('Testing Logic Module')
    print()
    test_pairs = test_data.logic_test_pairs
    ql = logic
    for i in range(len(test_pairs)):
        print('Rule[' + str(i + 1) + ']:')
        print('Time:\n\t' + str(((timeit(lambda: ql.train(test_pairs[i][0], test_pairs[i][1], 5000, ql.num_methods), number=1) / 1))))
        print()

    print('Testing programs:')
    print()
    c = 1
    for t in test_data.logic_search_data:
        print('Test[' + str(c) + ']')
        c += 1

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
        print('Time:')
        print('\t' + str("%.2f" % (ql.time_search(t, 10000) * 100000)) + 'us')
        print()

test_interoperability()
test_csd()
test_logic()

###################################################################################################
