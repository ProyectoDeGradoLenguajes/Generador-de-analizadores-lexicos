import sys
import graphviz as graph

estadoInicial = "q0"

class node(object):
    def __init__(self, estado, nombre):
        self.estado = estado
        self.nombre = nombre

def make_link_automata(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = token
    return G

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    return G

def make_node_arbol(nodesAutomata, estado, nombre):
    n = node(estado, nombre)
    nodesAutomata[nombre] = n
    return nombre

def make_node_automata(nodesArbol, aceptacion, nombre):
    n = node(aceptacion, nombre)
    nodesArbol[nombre] = n
    return nombre

def dibujarArbol(G, nombre_archivo):
    g2 = graph.Digraph(format='png')
    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(str(node2))
            g2.edge(str(node1), str(node2))
    filename = g2.render(filename='imgAutomatas/' + nombre_archivo)

def dibujarAutomata(G, nodesAutomata, nombre_archivo):
    global estadoInicial
    g2 = graph.Digraph(format='png')
    g2.attr("graph", _attributes={"rankdir": "LR"})
    g2.node("start", _attributes={"shape": "point",
                                  "color": "white", "fontcolor": "white"})
    g2.edge("start", estadoInicial)

    if len(G) < len(nodesAutomata):
        nameNode = "q" + str(len(nodesAutomata) - 1)
        g2.node(nameNode, _attributes={
                "shape": "doublecircle", "color": "black", "fontcolor": "black"})

    for node1 in G:
        nameNode = nodesAutomata[node1].nombre
        aceptacionNode = nodesAutomata[node1].estado

        if aceptacionNode:
            g2.node(nameNode, _attributes={
                    "shape": "doublecircle", "color": "black", "fontcolor": "black"})
        else:
            g2.node(nameNode, _attributes={"shape": "circle"})

        for node2 in G[node1]:
            etiqueta = str(G[node1][node2])
            g2.edge(str(node1), str(node2), label=etiqueta)

    filename = g2.render(filename='imgAutomatas/' + nombre_archivo)

def estrella_kleen(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    global estadoInicial
    nInicial = ""
    nFinal = ""
    if len(subArbol.keys()) > 1:
        nodo1 = list(subArbol.keys())[0]
        nodesAutomata[nodo1].estado = True
        nodo2 = list(subArbol.keys())[1]
        nodesAutomata[nodo2]. estado = True

        if nodesArbol[nodo1].estado == True:
            nInicial = nodo1
            nFinal = nodo2
        else:
            nInicial = nodo2
            nFinal = nodo1
    else:
        nodoPadre, estado = transicion(
            nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)

        nombre = "q" + str(estado - 2)
        nInicial = make_node_automata(nodesAutomata, True, nombre)

        nombre = "q" + str(estado - 1)
        nFinal = make_node_automata(nodesAutomata, True, nombre)
    
    make_link_automata(automata, nFinal, nInicial, "lambda")
    return nInicial, nFinal

def super_mas(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    nInicial, nFinal = estrella_kleen(
        nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)
    nodesAutomata[nInicial].estado = False
    make_link_automata(automata, nFinal, nInicial, "lambda")
    return nInicial, nFinal

def op_or(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    global estadoInicial

    nodosIniciales = []
    nodosFinales = []

    estado += 1
    nombre = "q" + str(estado)
    nInicial = make_node_automata(nodesAutomata, False, nombre)
    estadoInicial = nInicial
    estado += 1
    nombre = "q" + str(estado)
    nFinal = make_node_automata(nodesAutomata, True, nombre)

    for node1 in subArbol:
        for node2 in arbol[node1]:
            if nodesArbol[node2].estado:
                nodosIniciales.append(node2)
            else:
                nodosFinales.append(node2)
        del arbol[node1]
    make_link_automata(automata, nInicial, nodosIniciales.pop(0), "lambda")
    make_link_automata(automata, nInicial, nodosIniciales.pop(0), "lambda")

    make_link_automata(automata, nodosFinales.pop(0), nFinal, "lambda")
    make_link_automata(automata, nodosFinales.pop(0), nFinal, "lambda")
    del arbol[nodoPadre]
    return nInicial, nFinal

def op_and(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    global estadoInicial

    key1 = 0
    key2 = 0
    keys = list(subArbol.keys())
    if keys[0] < keys[1]:
        key1 = keys[0]
        key2 = keys[1]
    else:
        key1 = keys[1]
        key2 = keys[0]

    nodo1 = ""
    nodoInicial = ""
    for nodo in arbol[key1]:
        if nodesArbol[nodo].estado == False:
            nodo1 = nodo
        else:
            nodoInicial = nodo

    nodo2 = ""
    nodoFinal = ""
    for nodo in arbol[key2]:
        if nodesArbol[nodo].estado == True:
            nodo2 = nodo
        else:
            nodoFinal = nodo

    del arbol[key1]
    del arbol[key2]
    del arbol[nodoPadre]

    make_link(arbol, nodoPadre, nodoInicial)
    make_link(arbol, nodoPadre, nodoFinal)

    automata = make_link_automata(automata, nodo1, nodo2, "lambda")
    nodesAutomata[nodo1].estado = False

    if nodo2 == estadoInicial:
        estadoInicial = nodoInicial

    return nodoPadre, estado

def parentesis(nodoPadre, subArbol):
    dicOperaciones = {'*': estrella_kleen, '+': super_mas, '|': op_or}
    nodoAbuelo = nodoPadre + 1
    del subArbol['(']
    del subArbol[')']
    node1 = ""
    node2 = ""


    if len(subArbol.keys()) > 1:
        node1 = list(subArbol.keys())[0]
        node2 = list(subArbol.keys())[1]
        if type(node1) == int:
            make_link(arbol, nodoPadre, list(arbol[node1].keys())[0])
            make_link(arbol, nodoPadre, list(arbol[node1].keys())[1])
            del arbol[node1]
            del arbol[nodoPadre][node1]

        if type(node2) == int:
            make_link(arbol, nodoPadre, list(arbol[node2].keys())[0])
            make_link(arbol, nodoPadre, list(arbol[node2].keys())[1])
            del arbol[node2]
            del arbol[nodoPadre][node2]
            
    elif list(arbol[nodoAbuelo].keys())[0] in dicOperaciones or list(arbol[nodoAbuelo].keys())[1] in dicOperaciones:
        node1 = list(subArbol.keys())[0]
        make_link(arbol, nodoAbuelo, list(arbol[node1].keys())[0])
        make_link(arbol, nodoAbuelo, list(arbol[node1].keys())[1])
        del arbol[node1]
        del arbol[nodoPadre]
        del arbol[nodoAbuelo][nodoPadre]
        nodoPadre = nodoAbuelo
    else:
        node1 = list(arbol[nodoPadre].keys())[0]
        make_link(arbol, nodoPadre, list(arbol[node1].keys())[0])
        make_link(arbol, nodoPadre, list(arbol[node1].keys())[1])
        del arbol[node1]
        del arbol[nodoPadre][node1]
    
    return arbol[nodoPadre], nodoPadre


def sel_operacion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    if '(' in subArbol:
        subArbol, nodoPadre = parentesis(nodoPadre, subArbol)
        if len(subArbol)==2:
            return nodoPadre, estado   
        
    dicOperaciones = {'*': estrella_kleen, '+': super_mas, '|': op_or}
    operador = ""
    tamaño = len(subArbol)

    for i in subArbol:
        tamaño -= 1
        if i in dicOperaciones:
            operador = i
            tamaño += 1
        elif type(i) != int:
            tamaño += 1
        elif tamaño == 0:
            return op_and(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)
    
    operacion = dicOperaciones[operador]
    del subArbol[str(operador)]
    nInicialAutomata, nFinalAutomata = operacion(
        nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)

    nIncialArbol = make_node_arbol(nodesArbol, True, nInicialAutomata)
    nFinalArbol = make_node_arbol(nodesArbol, False, nFinalAutomata)
    make_link(arbol, nodoPadre, nIncialArbol)
    make_link(arbol, nodoPadre, nFinalArbol)
    estado += 2

    return nodoPadre, estado


def transicion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    token = list(subArbol.keys())[0]

    nombre = "q" + str(estado)
    if nombre in nodesAutomata:
        estado += 1
        nombre = "q" + str(estado)

    nInicialAutomata = make_node_automata(nodesAutomata, False, nombre)
    nInicialArbol = make_node_arbol(nodesArbol, True, nombre)

    estado += 1
    nombre = "q" + str(estado)
    nFinalAutomata = make_node_automata(nodesAutomata, True, nombre)
    nFinalArbol = make_node_arbol(nodesArbol, False, nombre)
    automata = make_link_automata(
        automata, nInicialAutomata, nFinalAutomata, token)

    del subArbol[token]

    make_link(arbol, nodoPadre, nInicialArbol)
    make_link(arbol, nodoPadre, nFinalArbol)

    estado += 1
    return nodoPadre, estado


def crearAutomata(arbol, operaciones):
    automata = {}
    nodesAutomata = {}
    nodesArbol = {}
    count = 0
    i = 1
    nodos = len(arbol)
    while i <= nodos:
        subArbol = arbol[i]
        if len(subArbol) > 1:
            i, count = sel_operacion(
                i, subArbol, automata, count, nodesAutomata, nodesArbol)
        else:
            i, count = transicion(
                i, subArbol, automata, count, nodesAutomata, nodesArbol)
        i += 1
    print(automata)
    dibujarAutomata(automata, nodesAutomata, "Automata")
    return automata, arbol

# prueba por funciones
#arbol = {1: {'a': 1, '*': 1}}
#arbol = {1: {'a': 1, '+': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1}, 4: {'c': 1}, 5: {3: 1, 4: 1}, 6: {'d': 1}, 7: {5: 1, 6: 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}}
#arbol = {1: {'a': 1, '*': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1}, 4: {'+': 1, 'c': 1}, 5: {'d': 1}, 6: {4: 1, 5: 1}, 7: {'|': 1, 3: 1, 6: 1}}
#arbol = {1: {'a': 1, '*': 1}, 2: {'+': 1, 'b': 1}, 3: {1: 1, 2: 1}, 4: {'x': 1}, 5: {3: 1, 4: 1}, 6: {'+': 1, 'c': 1}, 7: {'d': 1, '*': 1}, 8: {6: 1, 7: 1}, 9: {'y': 1}, 10: {8: 1, 9: 1}, 11: {10: 1, 5: 1, '|': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}, 4: {')': 1, 3: 1, '*': 1, '(': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}, 4: {')': 1, 3: 1, '+': 1, '(': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}, 4: {')': 1, 3: 1, '(': 1}, 5: {'+': 1, 4: 1}}
#arbol = {1: {'x': 1}, 2: {'a': 1}, 3: {'b': 1}, 4: {2: 1, 3: 1, '|': 1}, 5: {')': 1, 4: 1, '(': 1}, 6: {1: 1, 5: 1}, 7: {'y': 1}, 8: {6: 1, 7: 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {'|': 1, 1: 1, 2: 1}, 4: {'c': 1}, 5: {'|': 1, 3: 1, 4: 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}, 4: {'c': 1}, 5: {3: 1, 4: 1, '|': 1}, 6: {'d': 1}, 7: {5: 1, 6: 1, '|': 1}, 8: {'e': 1}, 9: {8: 1, '|': 1, 7: 1}, 10: {'f': 1}, 11: {9: 1, 10: 1, '|': 1}, 12: {'g': 1}, 13: {11: 1, 12: 1, '|': 1}, 14: {'e': 1}, 15: {13: 1, 14: 1, '|': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}, 4: {'c': 1}, 5: {3: 1, 4: 1, '|': 1}, 6: {'d': 1}, 7: {'|': 1, 5: 1, 6: 1}, 8: {')': 1, '*': 1, '(': 1, 7: 1}}
arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {'*': 1, ')': 1, '(': 1, 2: 1}, 4: {'+': 1, 'c': 1}, 5: {3: 1, 4: 1}, 6: {'*': 1, 'd': 1}, 7: {5: 1, 6: 1}, 8: {'|': 1, 1: 1, 7: 1}, 9: {8: 1, ')': 1, '(': 1}, 10: {'+': 1, 'e': 1}, 11: {'|': 1, 9: 1, 10: 1}}
# prueba arbol completo
#arbol = {1: {'a': 1}, 2: {'+': 1, 'x': 1}, 3: {'y': 1}, 4: {2: 1, 3: 1}, 5: {'(': 1, 4: 1, ')': 1}, 6: {'*': 1, 5: 1}, 7: {'*': 1, 'b': 1}, 8: {'c': 1}, 9: {8: 1, 7: 1}, 10: {9: 1, '(': 1, ')': 1}, 11: {10: 1, '+': 1}, 12: {11: 1, 6: 1, '|': 1}, 13: {'(': 1, 12: 1, ')': 1}, 14: {1: 1, 13: 1}, 15: {'s': 1}, 16: {14: 1, 15: 1}}

dicOperaciones = {'*': 1, '+': 1, '|': 1}

dibujarArbol(arbol, "arbolInicial")
automata, arbol = crearAutomata(arbol, dicOperaciones)
dibujarArbol(arbol, "arbolFinal")