import sys 
import spacy 
import re 
import math


 
def id(word):
     print(word , " => es un id")

 
def comparadores(word):
     print(word, " es un comparador")

 
def PresenteSimple(word):
	if re.search('(tion)$', word):
		print("<<", word, ">> => es un verbo en PresenteSimple")
		print("hello")
		return True
	return False
 
def numero(word):
     print(word, " => es un numero")

 
def retorno(word):
     print(word, " => reservada para retorno")

 
def palabra(word):
     pass

 
def log(word):
     print(word, " => reservada para impresion en pantalla")

 
def fin(word):
     print(word, " => reservada para finalizar sentencia")

 
def func(word):
     print(word , " => reservada para funcion")

 
def FuturoInperfecto(word):
	if re.search('(aba)$', word):
		print("<<", word, ">> => es un verbo en FuturoInperfecto")
		
		return True
	return False 
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
    AFD_id = {'q6': {'q3': ['palabra'], 'q1': ['numero']}, 'q3': {'q3': ['palabra'], 'q1': ['numero']}, 'q5': {'q6': ['palabra']}, 'q1': {'q3': ['palabra'], 'q1': ['numero']}}
    startState_id = 'q5'
    nodesAutomata_id = {'q6': True, 'q3': True, 'q5': False, 'q1': True}
    compoused_id = True

    AFD_comparadores = {'q10': {'q12': ['=']}, 'q5': {'q7': ['=']}, 'q24': {'q10': ['>'], 'q5': ['<'], 'q21': ['!'], 'q18': ['>'], 'q1': ['='], 'q15': ['<']}, 'q21': {'q23': ['=']}, 'q1': {'q3': ['=']}}
    startState_comparadores = 'q24'
    nodesAutomata_comparadores = {'q10': False, 'q3': True, 'q5': False, 'q23': True, 'q21': False, 'q12': True, 'q24': False, 'q18': True, 'q1': False, 'q15': True, 'q7': True}
    compoused_comparadores = False

    AFD_numero = {'q3': {'q6': ['two'], 'q21': ['seven'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q1': ['zero'], 'q24': ['eight'], 'q9': ['three'], 'q12': ['four'], 'q3': ['one']}, 'q27': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q21': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q6': {'q6': ['two'], 'q21': ['seven'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q1': ['zero'], 'q24': ['eight'], 'q9': ['three'], 'q12': ['four'], 'q3': ['one']}, 'q24': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q18': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q1': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q15': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q12': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}, 'q28': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q1': ['zero'], 'q24': ['eight'], 'q9': ['three'], 'q12': ['four'], 'q21': ['seven']}, 'q9': {'q6': ['two'], 'q3': ['one'], 'q18': ['six'], 'q27': ['nine'], 'q15': ['five'], 'q21': ['seven'], 'q1': ['zero'], 'q24': ['eight'], 'q12': ['four'], 'q9': ['three']}}
    startState_numero = 'q28'
    nodesAutomata_numero = {'q6': True, 'q3': True, 'q1': True, 'q21': True, 'q28': False, 'q12': True, 'q24': True, 'q18': True, 'q27': True, 'q15': True, 'q9': True}
    compoused_numero = False

    AFD_retorno = {'q0': {'q1': ['retorno']}, 'q1': {'q1': ['retorno']}}
    startState_retorno = 'q0'
    nodesAutomata_retorno = {'q0': True, 'q1': True}
    compoused_retorno = True

    AFD_palabra = {'q54': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q36': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q42': ['o'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q3': ['b'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q12': ['e'], 'q9': ['d']}, 'q72': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q42': ['o'], 'q33': ['l'], 'q27': ['j'], 'q1': ['a'], 'q6': ['c'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q63': ['v'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q3': ['b'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q12': ['e'], 'q48': ['q'], 'q9': ['d']}, 'q42': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q21': ['h'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q66': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q45': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q60': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q57': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q42': ['o'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q3': ['b'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q12': ['e'], 'q9': ['d']}, 'q75': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q27': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q15': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q63': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q9': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q6': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q39': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q3': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q1': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q76': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q21': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q69': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q51': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q12': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q30': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q24': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q21': ['h'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q18': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q21': ['h'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}, 'q33': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q36': ['m'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q9': ['d'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q18': ['g'], 'q27': ['j'], 'q15': ['f'], 'q63': ['v'], 'q48': ['q'], 'q21': ['h']}, 'q48': {'q72': ['y'], 'q39': ['n'], 'q57': ['t'], 'q3': ['b'], 'q33': ['l'], 'q1': ['a'], 'q6': ['c'], 'q42': ['o'], 'q54': ['s'], 'q69': ['x'], 'q66': ['w'], 'q51': ['r'], 'q75': ['z'], 'q12': ['e'], 'q45': ['p'], 'q30': ['k'], 'q60': ['u'], 'q24': ['i'], 'q27': ['j'], 'q18': ['g'], 'q36': ['m'], 'q15': ['f'], 'q21': ['h'], 'q63': ['v'], 'q48': ['q'], 'q9': ['d']}}
    startState_palabra = 'q76'
    nodesAutomata_palabra = {'q72': True, 'q54': True, 'q36': True, 'q66': True, 'q57': True, 'q45': True, 'q60': True, 'q75': True, 'q1': True, 'q15': True, 'q63': True, 'q9': True, 'q18': True, 'q6': True, 'q39': True, 'q3': True, 'q27': True, 'q76': False, 'q21': True, 'q69': True, 'q51': True, 'q12': True, 'q30': True, 'q24': True, 'q42': True, 'q33': True, 'q48': True}
    compoused_palabra = False

    AFD_log = {'q0': {'q1': ['log']}}
    startState_log = 'q0'
    nodesAutomata_log = {'q0': False, 'q1': True}
    compoused_log = True

    AFD_fin = {'q0': {'q1': ['e']}, 'q3': {'q5': ['d']}, 'q5': {'q1': ['e']}, 'q1': {'q3': ['n']}}
    startState_fin = 'q0'
    nodesAutomata_fin = {'q0': True, 'q3': False, 'q5': True, 'q1': False}
    compoused_fin = False

    AFD_func = {'q0': {'q1': ['func']}, 'q3': {'q5': ['o']}, 'q5': {'q7': ['n']}, 'q1': {'q3': ['i']}, 'q7': {'q1': ['func']}}
    startState_func = 'q0'
    nodesAutomata_func = {'q0': True, 'q3': False, 'q5': False, 'q1': False, 'q7': True}
    compoused_func = True

    AFDS = {'id' : AFD_id,'comparadores' : AFD_comparadores,'numero' : AFD_numero,'retorno' : AFD_retorno,'palabra' : AFD_palabra,'log' : AFD_log,'fin' : AFD_fin,'func' : AFD_func}
    start_states = {'id' : startState_id,'comparadores' : startState_comparadores,'numero' : startState_numero,'retorno' : startState_retorno,'palabra' : startState_palabra,'log' : startState_log,'fin' : startState_fin,'func' : startState_func}
    nodes_automatas = {'id' : nodesAutomata_id,'comparadores' : nodesAutomata_comparadores,'numero' : nodesAutomata_numero,'retorno' : nodesAutomata_retorno,'palabra' : nodesAutomata_palabra,'log' : nodesAutomata_log,'fin' : nodesAutomata_fin,'func' : nodesAutomata_func}
    is_compoused = {'id' : compoused_id,'comparadores' : compoused_comparadores,'numero' : compoused_numero,'retorno' : compoused_retorno,'palabra' : compoused_palabra,'log' : compoused_log,'fin' : compoused_fin,'func' : compoused_func}
    functions = {'id' : id,'comparadores' : comparadores,'numero' : numero,'retorno' : retorno,'palabra' : palabra,'log' : log,'fin' : fin,'func' : func}
    VERB_functions = {'PresenteSimple' : PresenteSimple,'FuturoInperfecto' : FuturoInperfecto}

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
                            is_conjugated=False
                            for function in VERB_functions.keys():
                                if VERB_functions[function](word):
                                    is_conjugated = True
                                    break
                            if not is_conjugated and w.pos_ == "VERB":
                                print("<<", word, ">> => es un verbo")                                    
                            else:                            
                                functions[id_AFD](word)
                    break
            if not result:
                unrecognized.append(word)
    print(" No se reconocio dentro del lenguaje, los siguientes caracteres:\n ", unrecognized)
    printMarkov(dictionaryYAFP, matrixes)
main()