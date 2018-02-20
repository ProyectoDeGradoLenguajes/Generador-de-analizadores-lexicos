import sys 
import math
def testFunction():
    print("hello YAFP!")

 
def letra():
     print('prueba joaquin')
 

def automata_Search(AFD, startState, nodesAutomata, word):
    numbers = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight",
               "9": "nine", "0": "zero"}
    isAcepted = False
    nextState = startState
    for symbol in word:
        if symbol in numbers:
            symbol = numbers[symbol]
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
          
    AFD_letra = {'q15': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q24': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q18': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q1': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q21': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q12': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q6': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q28': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q27': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q3': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}, 'q9': {'q15': ['f'], 'q9': ['d'], 'q24': ['i'], 'q1': ['a'], 'q21': ['h'], 'q12': ['e'], 'q6': ['c'], 'q18': ['g'], 'q3': ['b'], 'q27': ['j']}}
    startState_letra = 'q28'
    nodesAutomata_letra = {'q12': True, 'q24': True, 'q1': True, 'q27': True, 'q15': True, 'q6': True, 'q3': True, 'q9': True, 'q21': True, 'q28': False, 'q18': True}
    AFDS = {'letra' : AFD_letra}
    start_states = {'letra' : startState_letra}
    nodes_automatas = {'letra' : nodesAutomata_letra}
    functions = {'letra' : letra}

    word = sys.stdin.readline().strip('\n')
    word = list(map(str, word))

    for id_AFD in AFDS.keys():
        AFD = AFDS[id_AFD]
        startState = start_states[id_AFD]
        nodesAutomata = nodes_automatas[id_AFD]
        result = automata_Search(AFD, startState, nodesAutomata, word)
        if result:
            functions[id_AFD]()

while True:
    main()