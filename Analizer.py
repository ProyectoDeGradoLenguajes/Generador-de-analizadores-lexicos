import sysimport sys
import math


def test:
    print("test is ok")
    pass


def secondTest:
    print("Its alrigth dude")


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
    AFD = {'q2': {'q2': ['b'], 'q4': ['c'], 'q0': ['a']}, 'q7': {'q2': ['b'], 'q4': ['c'], 'q0': [
        'a']}, 'q0': {'q2': ['b'], 'q4': ['c'], 'q0': ['a']}, 'q4': {'q2': ['b'], 'q4': ['c'], 'q0': ['a']}}
    startState = 'q7'
    nodesAutomata = {'q2': True, 'q7': True, 'q0': True, 'q4': True}

    word = sys.stdin.readline().strip('\n')
    word = list(map(str, word))

    result = automata_Search(AFD, startState, nodesAutomata, word)
    print(result)


main()
