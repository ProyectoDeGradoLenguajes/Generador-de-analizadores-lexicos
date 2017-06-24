import sys
#import graphviz as graph

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    return G


def drawTree(G, etiqueta):
    g2 = graph.Digraph(format='png')
    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(str(node2))
            g2.edge(str(node1), str(node2))
    filename = g2.render(filename='img/g' + etiqueta)

def op_unary(tree, node, node_aux, character):
    ##arreglar
    if node_aux == 0 :
        node_aux = node - 1 

    if (len(tree[node-1]) > 1):
        tree = make_link(tree, node, node_aux)
        tree = make_link(tree, node, character)
        node += 1
    else:
        tree = make_link(tree, node_aux, character)
        
    return tree, node

def op_OR(tree, node, position_or, pair, character):
    if(len(position_or) == 0):
        position_or.append(node-1)
        pair = 0
    else:
        node1 = position_or.pop()
        node2 = node - 1
        tree = make_link(tree, node, node1)
        tree = make_link(tree, node, node2)
        tree = make_link(tree, node, '|')
        
        if character == '|':
            pair=0
            position_or.append(node)
        else:
            pair = 1
        
        node += 1
    return tree, node, position_or, pair

def op_concatenation(tree, node, node2, pair, character):
    
    if(character != ")"):
        if (type(character) is not int ):
            tree = make_link(tree, node, character)
            pair += 1
            node += 1

        if (node2 == 0):
            node2 = node - 2

        if (pair==2):
            tree = make_link(tree, node, node-1)
            tree = make_link(tree, node, node2)
            pair = 1
            node += 1
            
    return tree, node, pair



def makeSubTree(tree, sub_ER, node):
    unary_operations = {'*':op_unary,'+':op_unary}
    binary_operations = {'|':1,')':1}
    pair = 0;
    position_or = []
   
    sub_ER.pop(0)
    print(sub_ER)
    i = 0
    while i < len(sub_ER): 
        character = sub_ER[i]
        if type(character) is str:
            if character in unary_operations:
                tree, node = op_unary(tree, node, 0, character)
            elif character in binary_operations:
                tree, node, position_or, pair = op_OR(tree, node, position_or, pair, character)
            else:
               tree, node, pair = op_concatenation(tree, node, 0, pair, character)
        elif type(character) is int:
            if character in unary_operations:
                tree, node = op_unary(tree, node, sub_ER[i - 1], character)
            elif character in binary_operations:
                tree, node, position_or, pair = op_OR(tree, node, position_or, pair, character)
            elif(pair > 0):
                pair = 2
                node2 = character - 1
                tree, node, pair = op_concatenation(tree, node, node2, pair, character)
        print(tree)
        i+=1
    return tree, node 


def makeTree(ER):
    tree = {}
    node =  1

    parenthesis_position = []

    i = 0
    while i < len(ER):
        character = ER[i]
        if(character == "("):
            parenthesis_position.append(i)
       
        if(character == ")"):
            parenthesis = parenthesis_position.pop()
            sub_ER = ER[parenthesis:(i + 1)]
            tree, node = makeSubTree(tree, sub_ER, node)
            del ER[parenthesis:(i + 1)]
            ER.insert(parenthesis, node)
            i = parenthesis
        i += 1
        
    return tree


def arbolSignificado(fileER):
    #fileER = open('test/prueba.txt', 'r')
    for ER in fileER:
        # print "caso --->", i + 1
        ER = "(" + ER + ")"
        ER = list(map(str, ER))
        # ER almacenara una lista con el orden en que deben ser operados los
        # parentesis
        final_tree = makeTree(ER)

        #drawTree(final_tree, "finals")
        return final_tree


#print(arbolSignificado(["HolaMundo"]))
#print(arbolSignificado(["H+ola*Mundo+"]))
#print(arbolSignificado(["H|o|l|a"]))
#print(arbolSignificado(["mun(H|o|l|a)do"]))
#print(arbolSignificado(["mun(H|o|l|a)*do"]))
print(arbolSignificado(["(H|o)+|(l|a)*"]))
#print(arbolSignificado(["(x*y(b|d)(hola)+as*)+"]))
