import sys
import graphviz as graph
import Parse_Tree


class State(object):
    def __init__(self, aceptation, name):
        self.aceptation = aceptation
        self.name = name


def make_link_AFNe(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = token
    return G

def make_link_AFN(G, node1, node2, token):
    if node1 not in G:
        G[node1] = {}
    if node2 in G[node1]:
        (G[node1])[node2].append(token)
    else:
        (G[node1])[node2] = [token]
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
    g2.node("start", _attributes={"shape": "point",
                                  "color": "white", "fontcolor": "white"})
    g2.edge("start", "q" + str(startState))

    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(node1, _attributes={"shape": "circle"})
            g2.node(str(node2))
            g2.node(node2, _attributes={"shape": "circle"})
            g2.edge(str(node1), str(node2), label=G[node1][node2])

    for node1 in G:
        if nodesAutomata[node1].aceptation == True:
            g2.node(node1, _attributes={
                    "shape": "doublecircle", "color": "black", "fontcolor": "black"})
        for node2 in G[node1]:
            if nodesAutomata[node2].aceptation == True:
                g2.node(node2, _attributes={
                        "shape": "doublecircle", "color": "black", "fontcolor": "black"})

    filename = g2.render(filename='../graphs/automatas/' + nombre_archivo)


def delete_lambda(AFN, AFN_e, parent, u, neighbor):

    gfather = parent[u]
    father = u
    sons = AFN_e[u]

    print(gfather, father, sons)
    return AFN


def delete_limboState(AFN, nodesAutomata):
    i = 0
    while i < len(AFN):
        nodes1 = list(AFN.keys())
        node1 = nodes1[i]

        j = 0
        while j < len(AFN[node1]):
            nodes2 = list(AFN[node1].keys())
            node2 = nodes2[j]
            if node2 not in AFN and nodesAutomata[node2].aceptation == False:
                del AFN[node1][node2]
            j += 1
        i += 1
    return AFN


def DFS_AFN(AFN_e, startNode, nodesAutomata, symbol, AFN):
    word = ""
    color = {}
    parent = {}
    for v in AFN_e:
        color[v] = 'white'
    color[startNode] = 'gray'
    parent[startNode] = None
    nodelist = [startNode]
    while nodelist != []:
        u = nodelist.pop()
        for neighbor in AFN_e[u]:
            if color[neighbor] == 'white':
                color[neighbor] = 'gray'
                parent[neighbor] = u
                nodelist.append(neighbor)
            if AFN_e[u][neighbor] != "lambda":
                word = word + AFN_e[u][neighbor]
            if nodesAutomata[neighbor].aceptation:
                if word == symbol:
                    make_link_AFN(AFN,startNode,neighbor,symbol)
            if color[neighbor] == "black":
                word = ""
        color[u] = 'black'
    return AFN

def make_AFN(AFN_e, startState, nodesAutomata, alphabet):
    AFN = {}
    for node in nodesAutomata.keys():
        for symbol in alphabet:
            AFN = DFS_AFN(AFN_e, node, nodesAutomata, symbol, AFN)
    print(AFN)
    #drawAutomata(AFN, startState, nodesAutomata, "AFNfinal")
    return AFN


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
    AFN_e = make_link_AFNe(AFN_e, startNode, startNode1, "lambda")
    AFN_e = make_link_AFNe(AFN_e, startNode, startNode2, "lambda")

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
        AFN_e = make_link_AFNe(AFN_e, endNode, startNode2, "lambda")

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
        AFN_e = make_link_AFNe(AFN_e, endNode, startNode, "lambda")

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
        AFN_e = make_link_AFNe(AFN_e, endNode, startNode, "lambda")

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

    AFN_e = make_link_AFNe(AFN_e, startState, endState, token)

    state += 2
    return AFN_e, Tree, nodesAutomata, state


def select_transition(AFN_e, Tree, node, nodesAutomata, state, startState):
    subtree = Tree[node]

    if "|" in subtree:
        del subtree["|"]
        AFN_e, Tree, nodesAutomata, state, startState = transition_or(AFN_e, Tree, node, nodesAutomata, state,
                                                                      startState)
    elif "*" in subtree:
        del subtree["*"]
        AFN_e, Tree, nodesAutomata, state, startState = transition_kleen(AFN_e, Tree, node, nodesAutomata, state,
                                                                         startState)
    elif "+" in subtree:
        del subtree["+"]
        AFN_e, Tree, nodesAutomata, state, startState = transition_super(AFN_e, Tree, node, nodesAutomata, state,
                                                                         startState)
    else:
        AFN_e, Tree, nodesAutomata, state, startState = transition_concatenation(AFN_e, Tree, node, nodesAutomata,
                                                                                 state, startState)

    return AFN_e, Tree, nodesAutomata, state, startState


def makeAutomata():
    Tree, alphabet = Parse_Tree.parseTree()
    AFN_e = {}
    nodesAutomata = {}

    state = 0
    startState = 0

    i = 1
    while i < len(Tree) + 1:
        subtree = Tree[i]
        if len(subtree) == 1:
            AFN_e, Tree, nodesAutomata, state = transition(
                AFN_e, Tree, i, nodesAutomata, state)
        else:
            AFN_e, Tree, nodesAutomata, state, startState = select_transition(AFN_e, Tree, i, nodesAutomata, state,
                                                                              startState)
        i += 1
    drawAutomata(AFN_e, startState, nodesAutomata, "automata_final")
    AFN = make_AFN(AFN_e, startState, nodesAutomata, alphabet)


makeAutomata()
