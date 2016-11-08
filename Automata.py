class Node(object):
    def __init__(self, estado, nombre):
        self.estado = estado
        self.nombre = nombre    

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

def make_node_arbol(nodesAutomata, estado, nombre):
    n = Node(estado, nombre)
    nodesAutomata[nombre] = n
    return nombre

def make_node_automata(nodesArbol, aceptacion, nombre):
    n = Node(aceptacion, nombre)
    nodesArbol[nombre] = n
    return nombre  

def estrella_kleen(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    automata, estado = transicion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)
    nombre = "q" + str(estado - 2)
    nInicial = make_node_automata(nodesAutomata, True, nombre)
    nombre = "q" + str(estado - 1)
    nFinal = make_node_automata(nodesAutomata, False, nombre)
    
    make_link_automata(automata, nFinal, nInicial, "lambda")
    return nInicial, nFinal

def super_mas(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    automata, estado = transicion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)
    nombre = "q" + str(estado - 2)
    nInicial = make_node_automata(nodesAutomata, False, nombre)
    nombre = "q" + str(estado - 1)
    nFinal = make_node_automata(nodesAutomata, True, nombre)
    
    make_link_automata(automata, nFinal, nInicial, "lambda")
    return nInicial, nFinal

def sel_operacion (nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    dicOperaciones = {'*':estrella_kleen,'+':super_mas}
    nInicialAutomata = "" 
    nFinalAutomata = ""

    i = 0
    while i < len(list(subArbol.keys())):
        k = list(subArbol.keys())[i]
        print (k)
        i += 1
        if k in dicOperaciones:
            operacion = dicOperaciones[k] 
            del subArbol[k]
            nInicialAutomata, nFinalAutomata = operacion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)   
            break
    
    nInicialArbol = make_node_arbol(nodesArbol, True, nInicialAutomata)
    nFinalArbol = make_node_arbol(nodesArbol, False, nFinalAutomata)
    
    make_link(arbol, nodoPadre, nInicialArbol)
    make_link(arbol, nodoPadre, nFinalArbol)   
    
    estado += 2
    print ("operacion()")
    return automata, estado
    
def transicion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    token = list(subArbol.keys())[0]
    
    nombre = "q" + str(estado)
    nInicialAutomata = make_node_automata(nodesAutomata, False, nombre)
    nInicialArbol = make_node_arbol(nodesArbol, True, nombre)
    
    estado += 1
    nombre = "q" + str(estado)
    nFinalAutomata = make_node_automata(nodesAutomata, True, nombre)
    nFinalArbol = make_node_arbol(nodesArbol, False, nombre)
    
    automata = make_link_automata(automata, nInicialAutomata , nFinalAutomata, token)
       
    del subArbol[token]
    make_link(arbol, nodoPadre, nInicialArbol)
    make_link(arbol, nodoPadre, nFinalArbol)
    print ("transicion()")

    estado += 1
    return automata, estado

def crearAutomata(arbol, operaciones):
    automata={}
    nodesAutomata = {}
    nodesArbol = {}
    count = 0
    i = 1
    while i <= len(arbol):
        subArbol = arbol[i]
        if len(subArbol) > 1:
            automata, count = sel_operacion(i, subArbol, automata, count, nodesAutomata, nodesArbol)
        else:
            automata, count = transicion(i, subArbol, automata, count, nodesAutomata, nodesArbol)
            
        i += 1   
    return automata, arbol

#prueba por funciones
#arbol = {1: {'a': 1, '*': 1}}
arbol = {1: {'a': 1, '+': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}}

#prueba arbol completo
#arbol = {1: {'a': 1}, 2: {'+': 1, 'x': 1}, 3: {'y': 1}, 4: {2: 1, 3: 1}, 5: {'(': 1, 4: 1, ')': 1}, 6: {'*': 1, 5: 1}, 7: {'*': 1, 'b': 1}, 8: {'c': 1}, 9: {8: 1, 7: 1}, 10: {9: 1, '(': 1, ')': 1}, 11: {10: 1, '+': 1}, 12: {11: 1, 6: 1, '|': 1}, 13: {'(': 1, 12: 1, ')': 1}, 14: {1: 1, 13: 1}, 15: {'s': 1}, 16: {14: 1, 15: 1}}

dicOperaciones = {'*':1,'+':1}
automata, arbol = crearAutomata(arbol, dicOperaciones)




