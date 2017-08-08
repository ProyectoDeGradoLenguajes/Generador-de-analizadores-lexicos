import sys 
import sys
import math
 

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
          
    AFD = {'q4': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}, 'q7': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}, 'q2': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}, 'q0': {'q4': ['a'], 'q2': ['c'], 'q0': ['b']}}
    startState = 'q7'
    nodesAutomata = {'q4': True, 'q2': True, 'q0': True, 'q7': True}

    word = sys.stdin.readline().strip('\n')
    word = list(map(str, word))

    result = automata_Search(AFD, startState, nodesAutomata, word)
    print(result)

main()
