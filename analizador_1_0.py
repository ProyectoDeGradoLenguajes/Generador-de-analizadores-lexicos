import sys
import graphviz as graph

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

"""
Recibe una cadena que contiene la definicion del automata y una lista con la posicion de los parentesis
Retorna el arbol de significado

"""
def hacerArbol(automata):
    arbol = {}
    numNodo = 0
    pareja = 0
    i = 0
    while i < len(automata): 
        numNodo += 1
        token = automata[i]
        make_link(arbol, numNodo, token)
        pareja += 1
        i += 1
        if pareja == 2:
            numNodo += 1
            make_link(arbol, numNodo, numNodo-1)
            make_link(arbol, numNodo, numNodo-2)
            pareja -= 1         
            

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
        #Encierra todo el automata en un parentesis para garantizar que sea operado
        automata = sys.stdin.readline().strip()
        automata = list(map(str, automata))
        # automata almacenara una lista con el orden en que deben ser operados los parentesis
        arbolFinal = hacerArbol(automata)
        print (arbolFinal)
        dibujarArbol(arbolFinal, "finals")

programa()
