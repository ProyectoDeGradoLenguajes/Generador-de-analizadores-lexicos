import sys 
import math
def testFunction():
    print("hello YAFP!")

 
def id0_Print():
     print('seudoPalabra') 

def automata_Search(AFD, startState, nodesAutomata, word):
    isAcepted = False
    nextState = startState
    for symbol in word:
        state = nextState
        found = False
        for neighbor in AFD[state]:
            labels = AFD[state][neighbor]
            for label in labels:
                if label == symbol:
                    nextState = neighbor
                    found = True
                    break
        if not found:
            return isAcepted

    if nodesAutomata[nextState]:
        isAcepted = True
    return isAcepted

def main():
          
    AFD = {'q1': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q6': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q3': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q12': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q24': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q9': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q28': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q27': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q15': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q18': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}, 'q21': {'q27': ['j'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q24': ['i'], 'q9': ['d'], 'q18': ['g'], 'q3': ['b'], 'q6': ['c'], 'q15': ['f']}}
    startState = 'q28'
    nodesAutomata = {'q6': True, 'q12': True, 'q18': True, 'q9': True, 'q15': True, 'q1': True, 'q24': True, 'q28': False, 'q27': True, 'q3': True, 'q21': True}

    word = sys.stdin.readline().strip('\n')
    word = list(map(str, word))

    result = automata_Search(AFD, startState, nodesAutomata, word)

    if result:
        id0_Print()

    else:
        print(result)

    testFunction()

while True:
    main()
