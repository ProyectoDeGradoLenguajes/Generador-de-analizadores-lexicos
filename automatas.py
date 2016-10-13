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

def operacion (subArbol, automata): 
    print ("operacion()")
    return automata

def transicion(nodoPadre, subArbol, automata, estado):
    token = list(subArbol.keys())[0]
    node1 = "q" + str(estado)
    estado += 1
    node2 = "q" + str(estado)
    make_link_automata(automata, node1 , node2, token )
    estado += 1
    del subArbol[token]
    make_link(arbol, nodoPadre, node1)
    make_link(arbol, nodoPadre, node2)
    print ("transicion()")
    return automata, estado


arbol = {1: {'a': 1}, 2: {'+': 1, 'x': 1}, 3: {'y': 1}, 4: {2: 1, 3: 1}, 5: {'(': 1, 4: 1, ')': 1}, 6: {'*': 1, 5: 1}, 7: {'*': 1, 'b': 1}, 8: {'c': 1}, 9: {8: 1, 7: 1}, 10: {9: 1, '(': 1, ')': 1}, 11: {10: 1, '+': 1}, 12: {11: 1, 6: 1, '|': 1}, 13: {'(': 1, 12: 1, ')': 1}, 14: {1: 1, 13: 1}, 15: {'s': 1}, 16: {14: 1, 15: 1}}

#Lectura del arbol de significado
automata={}
count = 0
i = 1
while i <= len(arbol):
    subArbol = arbol[i]
    print (subArbol)
    if len(subArbol) > 1:
        automata = operacion(subArbol, automata)
    else:
        automata, count = transicion(i, subArbol, automata, count)
    print ("--------------------")
    i += 1
print (automata)