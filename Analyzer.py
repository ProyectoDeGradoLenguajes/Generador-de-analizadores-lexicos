import sys 
import spacy 
import re 
import math

palabras = 0
numeros = 0
ids = 0

def printResults():
    global letras
    global numeros
    global ids

    print("palabras = ", palabras, " mumeros = ", numeros, " ids = ", ids)

 
def palabra(word):
     print(word, "es una palabra")

 
def FuturoInperfecto(word):
	if re.search('era$', word):
		print("<<", word, ">> => es un verbo en FuturoInperfecto")
		print("futuro inperfecto")
		return True
	return False
 
def numero(word):
     print(word, "e s una numero")

 
def id(word):
     print(word , "es un id")
 
def mmult(A,B):
    AB = [[0 for k in range(len(B[0]))] for j in range(len(A))]
    for i,row in enumerate(A):
        for j,col in enumerate([list(c) for c in zip(*B)]):
            AB[i][j] = sum([a*b for a,b in zip(row,col)])
    return AB

def markovMatrix(matrixes): 
    hola_meaning = [[13.78,28.74,28.74,28.74,28.74],[24.9433,25.17,24.9433,24.9433],[24.9167,24.9167,25.25,24.9167],[21.4,21.4,21.4,35.8]]
    matrix_initial = [hola_meaning]
    if len(matrixes) == 0:
        for matrix in matrix_initial:
            matrixes.append(mmult(matrix,matrix))
    else:
        matrixes_new = []
        for i in range(len(matrixes)):
            matrixes_new.append(mmult(matrixes[i],matrix_initial[i]))
        matrixes = matrixes_new[:]
    return matrixes

def printMarkov(dicYAFP, matrixes):
    listYAFP = list(dicYAFP.keys())
    toString = ""
    i = 1
    j = 0
    for matrix in matrixes:
        if i == 1:
            toString =  toString + "\n" + listYAFP[j] + "_meaning :"
            j+=1
            i-=1            
        for i in range(len(matrix)):
            toString = toString + str(matrix[i][i]/100) + " ,"
    print(toString)

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
    nlp = spacy.load('es')
    unrecognized = []          
    AFD_palabra = {'q57': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q15': ['f'], 'q1': ['a'], 'q69': ['x'], 'q24': ['i'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q54': ['s'], 'q6': ['c'], 'q63': ['v'], 'q21': ['h'], 'q60': ['u'], 'q9': ['d'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q30': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q15': ['f'], 'q1': ['a'], 'q69': ['x'], 'q24': ['i'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q54': ['s'], 'q6': ['c'], 'q63': ['v'], 'q21': ['h'], 'q60': ['u'], 'q9': ['d'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q42': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q9': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q15': ['f'], 'q1': ['a'], 'q69': ['x'], 'q24': ['i'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q54': ['s'], 'q6': ['c'], 'q63': ['v'], 'q21': ['h'], 'q60': ['u'], 'q9': ['d'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q76': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q54': ['s'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q39': ['n'], 'q72': ['y'], 'q12': ['e'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q60': ['u'], 'q15': ['f'], 'q48': ['q'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q42': ['o']}, 'q1': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q51': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q3': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q63': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q6': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q45': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q21': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q33': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q54': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q18': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q69': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q27': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q15': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q75': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q72': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q12': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q24': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q60': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q54': ['s'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q39': ['n'], 'q72': ['y'], 'q12': ['e'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q60': ['u'], 'q15': ['f'], 'q48': ['q'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q42': ['o']}, 'q48': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q39': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q66': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}, 'q36': {'q57': ['t'], 'q30': ['k'], 'q45': ['p'], 'q9': ['d'], 'q69': ['x'], 'q1': ['a'], 'q75': ['z'], 'q51': ['r'], 'q12': ['e'], 'q72': ['y'], 'q60': ['u'], 'q6': ['c'], 'q63': ['v'], 'q24': ['i'], 'q21': ['h'], 'q54': ['s'], 'q15': ['f'], 'q48': ['q'], 'q42': ['o'], 'q3': ['b'], 'q18': ['g'], 'q33': ['l'], 'q66': ['w'], 'q36': ['m'], 'q27': ['j'], 'q39': ['n']}}
    startState_palabra = 'q76'
    nodesAutomata_palabra = {'q57': True, 'q30': True, 'q9': True, 'q60': True, 'q76': False, 'q1': True, 'q51': True, 'q63': True, 'q21': True, 'q3': True, 'q18': True, 'q27': True, 'q45': True, 'q15': True, 'q69': True, 'q75': True, 'q72': True, 'q12': True, 'q6': True, 'q24': True, 'q54': True, 'q48': True, 'q42': True, 'q33': True, 'q66': True, 'q36': True, 'q39': True}
    compoused_palabra = False

    AFD_numero = {'q15': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}, 'q1': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}, 'q28': {'q21': ['seven'], 'q15': ['five'], 'q9': ['three'], 'q18': ['six'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q3': ['one'], 'q24': ['eight']}, 'q12': {'q21': ['seven'], 'q27': ['nine'], 'q15': ['five'], 'q9': ['three'], 'q12': ['four'], 'q6': ['two'], 'q18': ['six'], 'q24': ['eight'], 'q3': ['one'], 'q1': ['zero']}, 'q24': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}, 'q6': {'q21': ['seven'], 'q27': ['nine'], 'q15': ['five'], 'q9': ['three'], 'q12': ['four'], 'q6': ['two'], 'q18': ['six'], 'q24': ['eight'], 'q3': ['one'], 'q1': ['zero']}, 'q21': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}, 'q27': {'q21': ['seven'], 'q27': ['nine'], 'q15': ['five'], 'q9': ['three'], 'q12': ['four'], 'q6': ['two'], 'q18': ['six'], 'q24': ['eight'], 'q3': ['one'], 'q1': ['zero']}, 'q9': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}, 'q3': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}, 'q18': {'q21': ['seven'], 'q9': ['three'], 'q15': ['five'], 'q1': ['zero'], 'q12': ['four'], 'q6': ['two'], 'q27': ['nine'], 'q24': ['eight'], 'q3': ['one'], 'q18': ['six']}}
    startState_numero = 'q28'
    nodesAutomata_numero = {'q15': True, 'q28': False, 'q12': True, 'q6': True, 'q1': True, 'q24': True, 'q21': True, 'q9': True, 'q3': True, 'q18': True, 'q27': True}
    compoused_numero = False

    AFD_id = {'q6': {'q3': ['palabra'], 'q1': ['numero']}, 'q5': {'q6': ['palabra']}, 'q3': {'q3': ['palabra'], 'q1': ['numero']}, 'q1': {'q3': ['palabra'], 'q1': ['numero']}}
    startState_id = 'q5'
    nodesAutomata_id = {'q6': False, 'q5': False, 'q3': True, 'q1': True}
    compoused_id = True

    AFDS = {'palabra' : AFD_palabra,'numero' : AFD_numero,'id' : AFD_id}
    start_states = {'palabra' : startState_palabra,'numero' : startState_numero,'id' : startState_id}
    nodes_automatas = {'palabra' : nodesAutomata_palabra,'numero' : nodesAutomata_numero,'id' : nodesAutomata_id}
    is_compoused = {'palabra' : compoused_palabra,'numero' : compoused_numero,'id' : compoused_id}
    functions = {'palabra' : palabra,'numero' : numero,'id' : id}
    VERB_functions = {'FuturoInperfecto' : FuturoInperfecto}

    name_file = sys.argv[1]

    sentences = open(name_file, encoding="utf8")



    matrixes = []
    dictionaryYAFP = {"mujer":0}
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
                    if word in dictionaryYAFP:
                        matrixes = markovMatrix(matrixes)[:]
                    doc = nlp(word)
                    for w in doc:
                        if w.pos_ == "VERB":
                            is_conjugated=False
                            for function in VERB_functions.keys():
                                if VERB_functions[function](word):
                                    is_conjugated = True
                                    break
                            if not is_conjugated:
                                print("<<", word, ">> => es un verbo")                                    
                        else:                            
                            functions[id_AFD](word)
                    break
            if not result:
                unrecognized.append(word)
    print(" No se reconocio dentro del lenguaje, los siguientes caracteres:\n ", unrecognized)
    printMarkov(dictionaryYAFP, matrixes)
    printResults()
main()