import sys

def make_link(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = token
    return G

def operacion (subArbol):
    print ("operacion()")

def transicion(subArbol):
    print ("transicion()")

arbol = {1: {'a': 1}, 2: {'x': 1, '+2': 1}, 3: {'y': 1}, 4: {2: 1, 3: 1}, 5: {4: 1, ')5': 1, '(5': 1}, 6: {'*6': 1, 5: 1}, 7: {'b': 1, '*7': 1}, 8: {'c': 1}, 9: {8: 1, 7: 1}, 10: {')10': 1, 9: 1, '(10': 1}, 11: {10: 1, '+11': 1}, 12: {'|12': 1, 11: 1, 6: 1}, 13: {')13': 1, 12: 1, '(13': 1}, 14: {1: 1, 13: 1}, 15: {'s': 1}, 16: {14: 1, 15: 1}}

i = 1
while i <= len(arbol):
    subArbol = arbol[i]
    print (subArbol)
    if len(subArbol) > 1:
        operacion(subArbol)
    else:
        transicion(subArbol)
    print ("--------------------")
    
    i += 1