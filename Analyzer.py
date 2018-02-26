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
          
    AFDS = {}
    start_states = {}
    nodes_automatas = {}
    functions = {}

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