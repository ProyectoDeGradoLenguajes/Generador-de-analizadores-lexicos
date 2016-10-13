import sys
import graphviz as graph

def make_link_automata(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = token
    return G

def make_link (G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    return G
def numEstado(estado):
    estado = list(map(str, estado))
    return int(estado[1])

def op_or(nodoPadre, subArbol, automata, estado):
    return "qx","qy"

def estrella_kleen(nodoPadre, subArbol, automata, estado):
    automata, estado = transicion(nodoPadre, subArbol, automata, estado)
    nInicial = "q" + str(estado - 2)
    nFinal = "q" + str(estado - 1)
    make_link_automata(automata, nFinal, nInicial, "lambda")
    make_link_automata(automata, nInicial, "aceptacion", "aceptado")
    return nInicial, nFinal

def super_mas(nodoPadre, subArbol, automata, estado):
    automata, estado = transicion(nodoPadre, subArbol, automata, estado)
    nInicial = "q" + str(estado - 2)
    nFinal = "q" + str(estado - 1)
    make_link_automata(automata, nFinal, nInicial, "lambda")
    make_link_automata(automata, nFinal, "aceptacion", "aceptado")
    return nInicial, nFinal

def parentesis_abre(nodoPadre, subArbol, automata, estado):
    return nInicial, nFinal

def parentesis_cierra(nodoPadre, subArbol, automata, estado):
    return nInicial, nFinal

def sel_operacion (nodoPadre, subArbol, automata, estado):
    dicOperaciones = {'*':estrella_kleen,'+':super_mas}
    nInicial = "" 
    nFinal = ""
    i = 0
    while i < len(list(subArbol.keys())):
        k = list(subArbol.keys())[i]
        print (k)
        i += 1
        if k in dicOperaciones:
            operacion = dicOperaciones[k] 
            del subArbol[k]
            nInicial, nFinal = operacion(nodoPadre, subArbol, automata, estado)   
            break
    make_link(arbol, nodoPadre, nInicial)
    make_link(arbol, nodoPadre, nFinal)   
    estado += 2
    print ("operacion()")
    return automata, estado

def transicion(nodoPadre, subArbol, automata, estado):
    token = list(subArbol.keys())[0]
    nInicial = "q" + str(estado)
    estado += 1
    nFinal = "q" + str(estado)
    make_link_automata(automata, nInicial , nFinal, token )
    estado += 1
    del subArbol[token]
    make_link(arbol, nodoPadre, nInicial)
    make_link(arbol, nodoPadre, nFinal)
     print ("transicion()")
    return automata, estado


arbol = {1: {'a': 1}, 2: {'+': 1, 'x': 1}, 3: {'y': 1}, 4: {2: 1, 3: 1}, 5: {'(': 1, 4: 1, ')': 1}, 6: {'*': 1, 5: 1}, 7: {'*': 1, 'b': 1}, 8: {'c': 1}, 9: {8: 1, 7: 1}, 10: {9: 1, '(': 1, ')': 1}, 11: {10: 1, '+': 1}, 12: {11: 1, 6: 1, '|': 1}, 13: {'(': 1, 12: 1, ')': 1}, 14: {1: 1, 13: 1}, 15: {'s': 1}, 16: {14: 1, 15: 1}}

dicOperaciones = {'*':1,'|':1,'+':1,'(':1,')':1}
#Lectura del arbol de significado
automata={}
count = 0
i = 1
while i <= len(arbol):
    subArbol = arbol[i]
    print (subArbol)
    if len(subArbol) > 1:
        print (subArbol)
        automata, count = sel_operacion(i, subArbol, automata, count)
    else:
        automata, count = transicion(i, subArbol, automata, count)
    print ("--------------------")
    i += 1

print (automata)