import sys
import graphviz as graph

cont = 0

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
    if len(tree[node_aux]) > 1:
        if "|" in tree[node_aux] and node_aux in tree[node-1]:
            del tree[node - 1]
            tree = make_link(tree, node - 1, character)
            tree = make_link(tree, node -1 , node_aux)

            tree = make_link(tree, node, node - 1)
            tree = make_link(tree, node, node - 2)
            node += 1
        
        elif "|" in tree[node_aux]:
            make_link(tree, node, node_aux)
            make_link(tree, node, character)
            node += 1           

        else:
            node_aux = node - 1 
            tree = make_link(tree, node_aux - 1, character)
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

def op_concatenation(tree, node, node1, node2, pair, character):
    flag = False
    if(character != ")"):               
        if (type(character) is not int ):
            flag = True 
            tree = make_link(tree, node, character)
            pair += 1
            node += 1

        if flag == True:
           node1 = node1 + 1
           node2 = node2 + 1

        if pair == 2:
            tree = make_link(tree, node, node1)
            tree = make_link(tree, node, node2)
            pair = 1
            node += 1

    return tree, node, pair



def makeSubTree(tree, sub_ER, node):
    global cont
    unary_operations = {'*':op_unary,'+':op_unary}
    binary_operations = {'|':1,')':1}
    pair = 0;
    position_or = []
   
    sub_ER.pop(0)
    #print(sub_ER)
    i = 0
    while i < len(sub_ER):
        cont += 1
        character = sub_ER[i]
        prev_character = sub_ER[i - 1]
        if type(prev_character) is int and sub_ER[i] in unary_operations:
            tree, node = op_unary(tree, node, prev_character-1, character)        
        elif type(character) is int:
            pair += 1
            if type(prev_character) is int:
                node1 = character - 1
                node2 = prev_character - 1
                tree, node, pair = op_concatenation(tree, node, node1, node2, pair, character)
            else:
                node1 = node - 1
                node2 = character - 1
                tree, node, pair = op_concatenation(tree, node, node1, node2, pair, character)

        elif type(character) is str:            
            if character in unary_operations:
                tree, node = op_unary(tree, node, 0, character)
            elif character in binary_operations:
                tree, node, position_or, pair = op_OR(tree, node, position_or, pair, character)
            else:
                node1 = node - 1
                node2 = node - 2
                tree, node, pair = op_concatenation(tree, node, node1, node2, pair, character)
        i+=1
        drawTree(tree, str(cont))
    return tree, node 


def makeTree(ER):
    tree = {}
    node =  1
    numbers = {"1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine", "0":"zero"}
    parenthesis_position = []

    i = 0
    while i < len(ER):
        character = ER[i]

        if character.isdigit():
             ER[i] = numbers[character]

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
        drawTree(final_tree, "finals")

        makeAutomata(final_tree)

class State(object):
    def __init__(self, aceptation, name):
        self.aceptation = aceptation
        self.name = name    

def make_link_automata(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = token
    return G

def make_link_tree(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = token
    return G

def make_state(nodesAutomata, aceptation, name):
    state = State(aceptation, name)
    nodesAutomata[name] = state
    return nodesAutomata

def drawAutomata(G, startState, nodesAutomata, nombre_archivo):
    g2 = graph.Digraph(format='png')
    g2.attr("graph", _attributes={"rankdir": "LR"})
    g2.node("start", _attributes={"shape":"point", "color":"white", "fontcolor":"white"})
    g2.edge("start", "q" + str(startState))
    
    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(node1, _attributes={"shape":"circle"})
            g2.node(str(node2))
            g2.node(node2, _attributes={"shape":"circle"})
            g2.edge(str(node1),str(node2),label=G[node1][node2])
    
    for node1 in G:
        if nodesAutomata[node1].aceptation == True:
            g2.node(node1, _attributes={"shape": "doublecircle", "color":"black", "fontcolor":"black"})
        for node2 in G[node1]:
             if nodesAutomata[node2].aceptation == True:
                g2.node(node2, _attributes={"shape": "doublecircle", "color":"black", "fontcolor":"black"})
    
    filename = g2.render(filename='imgAutomatas/'+ nombre_archivo)

def drawAFD (G, startState, nodesAutomata, nombre_archivo):
    g2 = graph.Digraph(format='png')
    g2.attr("graph", _attributes={"rankdir": "LR"})
    g2.node("start", _attributes={"shape":"point", "color":"white", "fontcolor":"white"})
    g2.edge("start", "q26")

    for node1 in G:
        for node2 in G[node1]:
            position = node2.find("_") 
            if position != -1:
                node_aux = node2[0:position]
                g2.node(node1, _attributes={"shape":"circle"})
                g2.node(node_aux, _attributes={"shape":"doublecircle"})
                g2.edge(str(node1), node_aux, label=G[node1][node2])
            else:
                g2.node(node1, _attributes={"shape":"circle"})
                g2.node(node2, _attributes={"shape":"doublecircle"})
                g2.edge(str(node1), node2, label=G[node1][node2])

    filename = g2.render(filename='imgAutomatas/AFDfinal')

def transition_or(AFN_e, Tree, node, nodesAutomata, state, startState):
    subtree = Tree[node]
    node1 = list(subtree.keys())[0]
    node2 = list(subtree.keys())[1]
    
    subAutomata1 = {}
    subAutomata2 = {}
    if node1 < node2:
        subAutomata1 = Tree[node1]
        subAutomata2 = Tree[node2]
    else:
        subAutomata1 = Tree[node2]
        subAutomata2 = Tree[node1]
       
    startNode1 = subAutomata1['start']
    endNodes1 = subAutomata1['end']
    startNode2 = subAutomata2['start']
    endNodes2 = subAutomata2['end']
  
    startNode = "q" + str(state)
    startState = state
    nodesAutomata = make_state(nodesAutomata, False, startNode)
    AFN_e = make_link_automata(AFN_e, startNode, startNode1, "lambda")
    AFN_e = make_link_automata(AFN_e, startNode, startNode2, "lambda")

    del Tree[node]
    endNodes = endNodes1 + endNodes2
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes)    

    state += 1
    return AFN_e, Tree, nodesAutomata, state, startState

def transition_concatenation(AFN_e, Tree, node, nodesAutomata, state, startState):
    subtree = Tree[node]
    node1 = list(subtree.keys())[0]
    node2 = list(subtree.keys())[1]
    
    subAutomata1 = {}
    subAutomata2 = {}
    if node1 < node2:
        subAutomata1 = Tree[node1]
        subAutomata2 = Tree[node2]
    else:
        subAutomata1 = Tree[node2]
        subAutomata2 = Tree[node1]
       
    startNode1 = subAutomata1['start']
    endNodes1 = subAutomata1['end']
    startNode2 = subAutomata2['start']
    endNodes2 = subAutomata2['end']

    for endNode in endNodes1:
        nodesAutomata[endNode].aceptation = False
        AFN_e = make_link_automata(AFN_e, endNode, startNode2, "lambda")

    startNode = startNode1
    del Tree[node]
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes2)

    startState = startNode.split('q')[1]     

    return AFN_e, Tree, nodesAutomata, state, startState

def transition_kleen(AFN_e, Tree, node, nodesAutomata, state, startState):
    node1 = list(Tree[node].keys())[0]
    subAutomata = Tree[node1]

    startNode = subAutomata['start']
    endNodes = subAutomata['end']

    nodesAutomata[startNode] = State(True, startNode)

    for endNode in endNodes:
        AFN_e = make_link_automata(AFN_e, endNode, startNode, "lambda")
    
    del Tree[node]
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes)

    return AFN_e, Tree, nodesAutomata, state, startState

def transition_super(AFN_e, Tree, node, nodesAutomata, state, startState):
    node1 = list(Tree[node].keys())[0]
    subAutomata = Tree[node1]

    startNode = subAutomata['start']
    endNodes = subAutomata['end']

    for endNode in endNodes:
        AFN_e = make_link_automata(AFN_e, endNode, startNode, "lambda")
    
    del Tree[node]
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes)

    return AFN_e, Tree, nodesAutomata, state, startState
    return AFN_e, Tree, nodesAutomata, state, startState

def transition(AFN_e, Tree, node, nodesAutomata, state):
    token = list(Tree[node].keys())[0]
    startState = "q" + str(state)
    endState = "q" + str(state + 1)

    nodesAutomata = make_state(nodesAutomata, False, startState)
    nodesAutomata = make_state(nodesAutomata, True, endState)

    startNode = startState
    endNodes = [endState]
    del Tree[node]
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes)

    AFN_e = make_link_automata(AFN_e, startState, endState, token)

    state += 2
    return AFN_e, Tree, nodesAutomata, state

def select_transition(AFN_e, Tree, node, nodesAutomata, state, startState):
    subtree = Tree[node]

    if "|" in subtree:
        del subtree["|"]
        AFN_e, Tree, nodesAutomata, state, startState = transition_or(AFN_e, Tree, node, nodesAutomata, state, startState)
    elif "*" in subtree:
        del subtree["*"]
        AFN_e, Tree, nodesAutomata, state, startState = transition_kleen(AFN_e, Tree, node, nodesAutomata, state, startState)    
    elif "+" in subtree:
        del subtree["+"]
        AFN_e, Tree, nodesAutomata, state, startState = transition_super(AFN_e, Tree, node, nodesAutomata, state, startState)        
    else:
        AFN_e, Tree, nodesAutomata, state, startState = transition_concatenation(AFN_e, Tree, node, nodesAutomata, state, startState)
    
    return AFN_e, Tree, nodesAutomata, state, startState

def delete_lambda(AFN, AFN_e, parent, u, neighbor):
    
    if AFN_e[u][neighbor] == "lambda":
        father = parent[u]
        son = u
        if father != None:
            while AFN_e[father][son] == "lambda":
                if parent[father] != None:
                    son = father
                    father = parent[father]
                else:
                    break;                   
            AFN = make_link_automata(AFN, father, neighbor, AFN_e[father][son])
    return AFN

def delete_limboState(AFN, nodesAutomata):
    i = 0
    while i<len(AFN):
        nodes1 = list(AFN.keys())
        node1 = nodes1[i]

        j = 0
        while j<len(AFN[node1]):
            nodes2 = list(AFN[node1].keys())
            node2 = nodes2[j]
            if node2 not in AFN and nodesAutomata[node2].aceptation == False:
                del AFN[node1][node2]
            j += 1
        i += 1
    return AFN


def make_AFN(AFN_e, startState, nodesAutomata):
    AFN = {}
    color = {}
    parent = {}
    startNode = "q" + str(startState)
    for v in AFN_e:
        color[v] = 'white'
    color[startNode] = 'gray'
    parent[startNode] = None
    nodelist = [startNode]
    repeat = False
    while nodelist != []:
        u = nodelist.pop()
        for neighbor in AFN_e[u]:
            if neighbor in color:
                if color[neighbor] == 'white':
                    color[neighbor] = 'gray'
                    parent[neighbor] = u
                    nodelist.append(neighbor)
                    AFN = delete_lambda(AFN, AFN_e, parent, u, neighbor)
                elif AFN_e[u][neighbor] == "lambda":
                    AFN = delete_lambda(AFN, AFN_e, parent, u, neighbor)   
            else:
                AFN =  make_link_automata(AFN, u, neighbor, AFN_e[u][neighbor])                           
        color[u] = 'black'
    
    AFN = delete_limboState(AFN, nodesAutomata) 
    drawAutomata(AFN, startState, nodesAutomata, "AFNfinal")   
    return AFN        

def make_AFD(AFN, nodesAutomata):

    AFD = {'q26': {'q20': 'zero'}, 'q20': {'q25_1': 'three', 'q25_2': 'five', 'q25_3': 'six', 'q25_4': 'seven', 'q25_5': 'eight', 'q25_6': 'nine', 'q25_7': 'one', 'q25_8': 'four', 'q25_9': 'two'}}
    drawAFD(AFD, 26, nodesAutomata, "AFDfinal")

def makeAutomata(Tree):
    AFN_e = {}
    nodesAutomata = {}

    state = 0
    startState = 0
    
    i = 1;
    while i < len(Tree) + 1:
        subtree = Tree[i]
        if len(subtree) == 1:
            AFN_e, Tree, nodesAutomata, state = transition(AFN_e, Tree, i, nodesAutomata, state)
        else:
            AFN_e, Tree, nodesAutomata, state, startState = select_transition(AFN_e, Tree, i, nodesAutomata, state, startState)
        i+=1
    drawAutomata(AFN_e, startState, nodesAutomata,"automata_final")
    AFN = make_AFN(AFN_e, startState, nodesAutomata)
    make_AFD(AFN, nodesAutomata)

#arbolSignificado(["HolaMundi"])
#arbolSignificado(["H+ola*Mundi+"])
#arbolSignificado(["H|o|l|a"])
#arbolSignificado(["mun(H|o|l|a)di"])
#arbolSignificado(["mun(H|o|l|a)*di"])
#arbolSignificado(["(H|o)+|(l|a)*"])
#arbolSignificado(["p(b|d)(hola)+z"])
#arbolSignificado(["(x*y(b|d)(hola)+is*)+"])
arbolSignificado(["0(1|2|3|4|5|6|7|8|9)*"])