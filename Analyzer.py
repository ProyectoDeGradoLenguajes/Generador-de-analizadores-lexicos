import sys 
import math
def testFunction():
    print("hello YAFP!")

 
def id():
     print('esto es un id')

 
def numero():
     print('esto es un numero')

 
def letra():
     print('esto es una letra')
 
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
          
    AFD_id = {'q6': {'q3': ['letra'], 'q1': ['numero']}, 'q5': {'q6': ['letra']}, 'q1': {'q3': ['letra'], 'q1': ['numero']}, 'q3': {'q3': ['letra'], 'q1': ['numero']}}
    startState_id = 'q5'
    nodesAutomata_id = {'q6': True, 'q5': False, 'q3': True, 'q1': True}
    compoused_id = True

    AFD_numero = {'q28': {'q6': ['two'], 'q27': ['nine'], 'q15': ['five'], 'q1': ['zero'], 'q3': ['one'], 'q9': ['three'], 'q21': ['seven'], 'q24': ['eight'], 'q12': ['four'], 'q18': ['six']}, 'q18': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q12': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q6': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q15': {'q6': ['two'], 'q27': ['nine'], 'q15': ['five'], 'q1': ['zero'], 'q3': ['one'], 'q9': ['three'], 'q21': ['seven'], 'q24': ['eight'], 'q12': ['four'], 'q18': ['six']}, 'q27': {'q6': ['two'], 'q27': ['nine'], 'q15': ['five'], 'q1': ['zero'], 'q3': ['one'], 'q9': ['three'], 'q21': ['seven'], 'q24': ['eight'], 'q12': ['four'], 'q18': ['six']}, 'q21': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q3': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q24': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q9': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}, 'q1': {'q6': ['two'], 'q3': ['one'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q27': ['nine'], 'q21': ['seven'], 'q24': ['eight'], 'q9': ['three'], 'q18': ['six']}}
    startState_numero = 'q28'
    nodesAutomata_numero = {'q28': False, 'q12': True, 'q6': True, 'q15': True, 'q27': True, 'q21': True, 'q3': True, 'q24': True, 'q9': True, 'q1': True, 'q18': True}
    compoused_numero = False

    AFD_letra = {'q63': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q51': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q69': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q66': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q6': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q45': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q60': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q33': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q27': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q9': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q24': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q42': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q75': ['z'], 'q36': ['m'], 'q72': ['y']}, 'q36': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q18': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q48': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q54': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q12': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q15': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q57': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q3': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q30': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q21': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q39': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q76': {'q48': ['q'], 'q27': ['j'], 'q54': ['s'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q72': ['y'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q63': ['v'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q18': ['g'], 'q36': ['m'], 'q75': ['z']}, 'q1': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q75': ['z'], 'q18': ['g'], 'q36': ['m'], 'q72': ['y']}, 'q72': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q75': ['z'], 'q18': ['g'], 'q36': ['m'], 'q72': ['y']}, 'q75': {'q48': ['q'], 'q27': ['j'], 'q63': ['v'], 'q51': ['r'], 'q69': ['x'], 'q66': ['w'], 'q12': ['e'], 'q57': ['t'], 'q6': ['c'], 'q45': ['p'], 'q60': ['u'], 'q15': ['f'], 'q42': ['o'], 'q21': ['h'], 'q9': ['d'], 'q33': ['l'], 'q3': ['b'], 'q54': ['s'], 'q30': ['k'], 'q24': ['i'], 'q39': ['n'], 'q1': ['a'], 'q75': ['z'], 'q18': ['g'], 'q36': ['m'], 'q72': ['y']}}
    startState_letra = 'q76'
    nodesAutomata_letra = {'q57': True, 'q63': True, 'q51': True, 'q69': True, 'q66': True, 'q6': True, 'q45': True, 'q60': True, 'q33': True, 'q42': True, 'q27': True, 'q9': True, 'q24': True, 'q36': True, 'q18': True, 'q48': True, 'q54': True, 'q12': True, 'q15': True, 'q21': True, 'q3': True, 'q30': True, 'q39': True, 'q76': False, 'q1': True, 'q72': True, 'q75': True}
    compoused_letra = False

    AFDS = {'id' : AFD_id,'numero' : AFD_numero,'letra' : AFD_letra}
    start_states = {'id' : startState_id,'numero' : startState_numero,'letra' : startState_letra}
    nodes_automatas = {'id' : nodesAutomata_id,'numero' : nodesAutomata_numero,'letra' : nodesAutomata_letra}
    is_compoused = {'id' : compoused_id,'numero' : compoused_numero,'letra' : compoused_letra}
    functions = {'id' : id,'numero' : numero,'letra' : letra}

    word = sys.stdin.readline().strip('\n')
    word = list(map(str, word))

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
            functions[id_AFD]()
            break
    if not result:
        print("No se reconoce dentro del lenguaje")

while True:
    main()