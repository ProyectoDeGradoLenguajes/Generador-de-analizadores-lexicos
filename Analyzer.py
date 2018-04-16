import sys 
import math

 
def menos(word):
     print("MINUS")

 
def nuemro(word):
     print("NUMBER")
 
def compoused_automata_Search(AFD, startState, nodesAutomata, word, AFDS, start_states, nodes_automatas):
    isAcepted = False
    nextState = startState
    count = 0
    for symbol in word:
        state = nextState
        found = False
        for neighbor in AFD[state]:
            labels = AFD[state][neighbor]
            for label in labels:
                if label in AFDS:
                    sub_automata = automata_Search(
                        AFDS[label], start_states[label], nodes_automatas[label], symbol)
                    if sub_automata:
                        count += 1
                        found = True
                    elif not sub_automata and count > 0:
                        nextState = neighbor
                        found = True
                        count = 0
                elif label == symbol:
                    nextState = neighbor
                    found = True
                    break

        if not found:
            return isAcepted

    if nodesAutomata[nextState]:
        isAcepted = True
    return isAcepted


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
          
    AFD_menos = {'q0': {'q1': ['-']}}
    startState_menos = 'q0'
    nodesAutomata_menos = {'q0': False, 'q1': True}
    compoused_menos = False

    AFD_nuemro = {'q27': {'q18': ['six'], 'q12': ['four'], 'q21': ['seven'], 'q15': ['five'], 'q9': ['three'], 'q1': ['zero'], 'q3': ['one'], 'q24': ['eight'], 'q6': ['two'], 'q27': ['nine']}, 'q6': {'q18': ['six'], 'q12': ['four'], 'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q9': ['three'], 'q27': ['nine'], 'q24': ['eight'], 'q21': ['seven'], 'q1': ['zero']}, 'q18': {'q18': ['six'], 'q12': ['four'], 'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q9': ['three'], 'q27': ['nine'], 'q24': ['eight'], 'q21': ['seven'], 'q1': ['zero']}, 'q12': {'q18': ['six'], 'q12': ['four'], 'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q9': ['three'], 'q27': ['nine'], 'q24': ['eight'], 'q21': ['seven'], 'q1': ['zero']}, 'q15': {'q18': ['six'], 'q12': ['four'], 'q21': ['seven'], 'q15': ['five'], 'q9': ['three'], 'q1': ['zero'], 'q3': ['one'], 'q24': ['eight'], 'q6': ['two'], 'q27': ['nine']}, 'q9': {'q9': ['three'], 'q18': ['six'], 'q12': ['four'], 'q21': ['seven'], 'q15': ['five'], 'q3': ['one'], 'q27': ['nine'], 'q24': ['eight'], 'q6': ['two'], 'q1': ['zero']}, 'q24': {'q9': ['three'], 'q18': ['six'], 'q12': ['four'], 'q21': ['seven'], 'q15': ['five'], 'q3': ['one'], 'q27': ['nine'], 'q24': ['eight'], 'q6': ['two'], 'q1': ['zero']}, 'q21': {'q9': ['three'], 'q18': ['six'], 'q12': ['four'], 'q21': ['seven'], 'q15': ['five'], 'q3': ['one'], 'q27': ['nine'], 'q24': ['eight'], 'q6': ['two'], 'q1': ['zero']}, 'q28': {'q18': ['six'], 'q12': ['four'], 'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q9': ['three'], 'q27': ['nine'], 'q24': ['eight'], 'q21': ['seven'], 'q1': ['zero']}, 'q1': {'q18': ['six'], 'q12': ['four'], 'q21': ['seven'], 'q15': ['five'], 'q9': ['three'], 'q1': ['zero'], 'q3': ['one'], 'q24': ['eight'], 'q6': ['two'], 'q27': ['nine']}, 'q3': {'q18': ['six'], 'q12': ['four'], 'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q9': ['three'], 'q27': ['nine'], 'q24': ['eight'], 'q21': ['seven'], 'q1': ['zero']}}
    startState_nuemro = 'q28'
    nodesAutomata_nuemro = {'q21': True, 'q27': True, 'q15': True, 'q18': True, 'q12': True, 'q3': True, 'q24': True, 'q6': True, 'q28': False, 'q9': True, 'q1': True}
    compoused_nuemro = False

    AFDS = {'menos' : AFD_menos,'nuemro' : AFD_nuemro}
    start_states = {'menos' : startState_menos,'nuemro' : startState_nuemro}
    nodes_automatas = {'menos' : nodesAutomata_menos,'nuemro' : nodesAutomata_nuemro}
    is_compoused = {'menos' : compoused_menos,'nuemro' : compoused_nuemro}
    functions = {'menos' : menos,'nuemro' : nuemro}

    sentences = [sys.stdin.readline().strip('\n')]
             
    for sentence in sentences:
        words = sentence.split(' ')   
        for word in words:
            result = False
            for id_AFD in AFDS.keys():
                AFD = AFDS[id_AFD]
                startState = start_states[id_AFD]
                nodesAutomata = nodes_automatas[id_AFD]
                if is_compoused[id_AFD]:
                    result = compoused_automata_Search(
                        AFD, startState, nodesAutomata, word, AFDS, start_states, nodes_automatas)
                else:
                    result = automata_Search(AFD, startState, nodesAutomata, word)
                if result:
                    functions[id_AFD](word)
                    break
            if not result:
                print("No se reconoce dentro del lenguaje")

while True:
    main()