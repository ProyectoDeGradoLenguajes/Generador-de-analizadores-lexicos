import sys
import graphviz as graph

dicOperaciones = {}
pilaNodos = []
pilaOperaciones = []
pilaParentesis = []
numNodo = 0
pareja = 0

"""
 Crea conexiones para grafos unidireccionales
"""
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    return G

"""
Recibe el arbol de significado y el nombre que tendra el archivo
Utiliza la libreria graphviz para pintar el arbol de significado
"""
def dibujarArbol(G,etiqueta):
    g2 = graph.Digraph(format='png')
    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(str(node2))
            g2.edge(str(node1),str(node2))
    filename = g2.render(filename='img/g'+ etiqueta)

def manejoOperaciones(token,arbol):
    dicbinarias = {'|':op_or,'fin':0}
    dicUnarias = {'*':op_estrellaKleen,'+':op_superMas}
    global pareja
    pareja = 0
    if token in dicbinarias:
        if len(pilaOperaciones) <= 0:
            pilaOperaciones.append(token)
            pilaNodos.append(numNodo)
            return
        else:
            operacion = dicOperaciones[pilaOperaciones.pop()]
            operacion(arbol)
            pilaOperaciones.append(token)
            pilaNodos.append(numNodo)
    else:
        pilaOperaciones.append(token)
        pilaNodos.append(numNodo)
        operacion = dicOperaciones[pilaOperaciones.pop()]
        operacion(arbol)

def op_or(arbol):
    global numNodo
    nodo1 = numNodo
    numNodo += 1
    nodo2 = pilaNodos.pop()
    make_link(arbol, numNodo, nodo1)
    make_link(arbol, numNodo, nodo2)
    make_link(arbol, numNodo, '|'+str(numNodo))
    print ("operacion or")

def op_estrellaKleen(arbol):
    global pareja
    nodo1 = pilaNodos.pop()
    if len(arbol[nodo1]) > 1:
        make_link(arbol, nodo1 - 1, '*'+str(nodo1-1))
    else:
        make_link(arbol, nodo1, '*'+str(nodo1))
    pareja += 1    
    print ("operacion estrella de kleen")
def op_superMas(arbol):
    global pareja
    nodo1 = pilaNodos.pop()
    if len(arbol[nodo1]) > 1:
        make_link(arbol, nodo1 - 1, '+'+str(nodo1-1))
    else:
        make_link(arbol, nodo1, '+'+str(nodo1))
    pareja += 1    
    print ("operacion super mas")
def parentesisA(arbol):
    pilaParentesis.append(pilaNodos.pop())
    print ("parentesis que abre")
def parentesisB(arbol):
    pilaNodos.pop()
    """
    verifica que no existan operaciones pendientes dentro 
    de los parentesis para realizarlas antes de cerrar los parentesis
    """
    while len(pilaOperaciones) > 0:
        operacion = dicOperaciones[pilaOperaciones.pop()]
        operacion(arbol)
    
    global numNodo
    global pareja
    """
    Incluye un nuevo nodo con los parentesis para hacer refencia 
    a la expresion regular que esta denrto de los parentesis
    """"
    nodo1 = numNodo
    numNodo += 1
    make_link(arbol, numNodo, '('+str(numNodo))
    make_link(arbol, numNodo, ')'+str(numNodo))
    make_link(arbol, numNodo, numNodo - 1)
    #Une la expresion regular del parentesis con el resto del arbol
    numNodo += 1
    nodo2 = pilaParentesis.pop()
    make_link(arbol, numNodo, nodo1+1)
    make_link(arbol, numNodo, nodo2)
    pareja += 1
    print ("parentesis que cierra")
       

"""
Recibe una cadena que contiene la definicion del automata y una lista con la posicion de los parentesis
Retorna el arbol de significado
"""
def hacerArbol(automata):
    global numNodo
    global pareja
    global dicOperaciones
    dicOperaciones = {'*':op_estrellaKleen,'|':op_or,'+':op_superMas,'(':parentesisA,')':parentesisB,'fin':0}
    arbol = {}
    i = 0
    while i < len(automata):
        token = automata[i]
        #busqueda en el diccionario de la funcion que desarrolla la funcion
        if token in dicOperaciones:
            manejoOperaciones(token,arbol)
        else:
            #generacion de la relacion simple nodo - token
            numNodo += 1
            make_link(arbol, numNodo, token)
            pareja += 1
        i += 1
        #operacion and
        if pareja == 2:
            numNodo += 1
            make_link(arbol, numNodo, numNodo-1)
            make_link(arbol, numNodo, numNodo-2)
            pareja -= 1  
    print ()
    manejoOperaciones('fin',arbol)   
    return arbol
    
"""
Lee el archivo de entrada y delega el procesamiento por fases.
    1) Crear el arbol de significado
    2) Dibuja el arbol de significado
    4) Recorre el arbol de significado
"""
def programa():
    numAutomatas = int(sys.stdin.readline().strip())
    for i in range(numAutomatas):
        ##print "caso --->", i + 1
        automata = sys.stdin.readline().strip()
        automata = list(map(str, automata))
        # automata almacenara una lista con el orden en que deben ser operados los parentesis
        arbolFinal = hacerArbol(automata)
        print (arbolFinal)
        dibujarArbol(arbolFinal, "finals")

programa()