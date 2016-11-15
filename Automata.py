class node(object):
    def __init__(self, estado, nombre):
        self.estado = estado
        self.nombre = nombre    

import sys
import graphviz as graph
estadoInicial = "q0"

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
    n = node(estado, nombre)
    nodesAutomata[nombre] = n
    return nombre

def make_node_automata(nodesArbol, aceptacion, nombre):
    n = node(aceptacion, nombre)
    nodesArbol[nombre] = n
    return nombre  
######################################################################################################
def dibujarArbol(G,nombre_archivo):
    g2 = graph.Digraph(format='png')
    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(str(node2))
            g2.edge(str(node1),str(node2))
    filename = g2.render(filename='imgAutomatas/'+ nombre_archivo)

def dibujarAutomata(G ,nodesAutomata ,nombre_archivo):
    print(G.keys())
    print(nodesAutomata.keys())
    global estadoInicial
    g2 = graph.Digraph(format='png')
    g2.attr("graph", _attributes={"rankdir": "LR"})

    g2.node("start", _attributes={"shape":"point", "color":"white", "fontcolor":"white"})
    g2.edge("start", estadoInicial)

    if len(G) < len(nodesAutomata):
        nameNode = "q" + str(len(nodesAutomata)-1)
        g2.node(nameNode, _attributes={"shape": "doublecircle", "color":"black", "fontcolor":"black"})

    for node1 in G:
        nameNode = nodesAutomata[node1].nombre
        aceptacionNode = nodesAutomata[node1].estado
    
        if aceptacionNode:
            g2.node(nameNode, _attributes={"shape": "doublecircle", "color":"black", "fontcolor":"black"})
        else:
            g2.node(nameNode, _attributes={"shape":"circle"})
        
        for node2 in G[node1]:
            etiqueta = str(G[node1][node2])
            g2.edge(str(node1), str(node2), label=etiqueta)
    
    
    
    filename = g2.render(filename='imgAutomatas/'+ nombre_archivo)
    
#####################################################################################################33333333
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
    
    return nInicial, nFinal

def op_and(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
    key1 = 0
    key2 = 0
    for key in subArbol:
        if key > key2:
            key1 = key2
            key2 = key
        else:
            key1 = key
    
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
  
    return automata, estado

def sel_operacion (nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol):
        
    dicOperaciones = {'*':estrella_kleen,'+':super_mas,'|':op_or}
    operador = ""
    token = ""
    tamaño = len(subArbol)
    print (subArbol)
    print (len(subArbol))
    for i in subArbol:
        tamaño -= 1
        if i in dicOperaciones:
            operador = i
            tamaño += 1
        elif type(i) != int:
            token = i
            tamaño += 1
        elif tamaño == 0:
            return op_and(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)
        
            

    operacion = dicOperaciones[operador]
    del subArbol[str(operador)]
    nInicialAutomata ,nFinalAutomata = operacion(nodoPadre, subArbol, automata, estado, nodesAutomata, nodesArbol)

    nIncialArbol = make_node_arbol(nodesArbol,True,nInicialAutomata)
    nFinallArbol = make_node_arbol(nodesArbol,False,nFinalAutomata)
    make_link(arbol,nodoPadre,nIncialArbol)
    make_link(arbol,nodoPadre,nIncialArbol)

    estado += 2

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

    estado += 1
    return automata, estado

def crearAutomata(arbol, operaciones):
    automata={}
    nodesAutomata = {}
    nodesArbol = {}
    count = 0
    i = 1
    nodos = len(arbol)
    while i <= nodos:
        print(i)
        subArbol = arbol[i]
        if len(subArbol) > 1:
            automata, count = sel_operacion(i, subArbol, automata, count, nodesAutomata, nodesArbol)
        else:
            automata, count = transicion(i, subArbol, automata, count, nodesAutomata, nodesArbol)
        dibujarArbol(arbol,"arbolFinal"+str(i))
        i += 1
    print (automata)
    dibujarAutomata(automata,nodesAutomata,"Automata")
    return automata, arbol

#prueba por funciones
#arbol = {1: {'a': 1, '*': 1}}
#arbol = {1: {'a': 1, '+': 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1}, 4: {'c': 1}, 5: {3: 1, 4: 1}, 6: {'d': 1}, 7: {5: 1, 6: 1}}
#arbol = {1: {'a': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1, '|': 1}}
#arbol = {1: {'a': 1, '*': 1}, 2: {'b': 1}, 3: {1: 1, 2: 1}, 4: {'+': 1, 'c': 1}, 5: {'d': 1}, 6: {4: 1, 5: 1}, 7: {'|': 1, 3: 1, 6: 1}}
arbol = {1: {'a': 1, '*': 1}, 2: {'+': 1, 'b': 1}, 3: {1: 1, 2: 1}, 4: {'x': 1}, 5: {3: 1, 4: 1}, 6: {'+': 1, 'c': 1}, 7: {'d': 1, '*': 1}, 8: {6: 1, 7: 1}, 9: {'y': 1}, 10: {8: 1, 9: 1}, 11: {10: 1, 5: 1, '|': 1}}
#prueba arbol completo
#arbol = {1: {'a': 1}, 2: {'+': 1, 'x': 1}, 3: {'y': 1}, 4: {2: 1, 3: 1}, 5: {'(': 1, 4: 1, ')': 1}, 6: {'*': 1, 5: 1}, 7: {'*': 1, 'b': 1}, 8: {'c': 1}, 9: {8: 1, 7: 1}, 10: {9: 1, '(': 1, ')': 1}, 11: {10: 1, '+': 1}, 12: {11: 1, 6: 1, '|': 1}, 13: {'(': 1, 12: 1, ')': 1}, 14: {1: 1, 13: 1}, 15: {'s': 1}, 16: {14: 1, 15: 1}}

dicOperaciones = {'*':1,'+':1,'|':1}

dibujarArbol(arbol,"arbolInicial")
automata, arbol = crearAutomata(arbol, dicOperaciones)
dibujarArbol(arbol,"arbolFinal")





