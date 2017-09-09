import sys 
import math
def testFunction():
    print("hello YAFP!")

 
def id0_Print():
     print('is_a_number') 

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
          
    AFD = {'q2': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}, 'q0': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}, 'q4': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}, 'q7': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}}
    startState = 'q7'
    nodesAutomata = {'q2': True, 'q0': True, 'q4': True, 'q7': True}

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
