import sys
import graphviz as graph
import package.Parse_Tree


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
    nodesAutomata[name] = aceptation
    return nodesAutomata


def drawAFN(G, startState, nodesAutomata, nombre_archivo):
    g2 = graph.Digraph(format='png')
    g2.attr("graph", _attributes={"rankdir": "LR"})
    g2.node("start", _attributes={"shape": "point",
                                  "color": "white", "fontcolor": "white"})
    g2.edge("start", "q" + str(startState))
    for node1 in G:
        if nodesAutomata[node1] == True:
            g2.node(node1, _attributes={
                    "shape": "doublecircle", "color": "black", "fontcolor": "black"})
        else:
            g2.node(str(node1))
            g2.node(node1, _attributes={"shape": "circle"})

        for node2 in G[node1]:
            if nodesAutomata[node2] == True:
                g2.node(node2, _attributes={
                        "shape": "doublecircle", "color": "black", "fontcolor": "black"})
            else:
                g2.node(str(node2))
                g2.node(node2, _attributes={"shape": "circle"})
            for _label_ in G[node1][node2]:
                g2.edge(str(node1), str(node2), label=_label_)
    filename = g2.render(filename='graphs/automatas/' + nombre_archivo)


def drawAFNe(G, startState, nodesAutomata, nombre_archivo):
    g2 = graph.Digraph(format='png')
    g2.attr("graph", _attributes={"rankdir": "LR"})
    g2.node("start", _attributes={"shape": "point",
                                  "color": "white", "fontcolor": "white"})
    g2.edge("start", "q" + str(startState))

    for node1 in G:
        if nodesAutomata[node1] == True:
            g2.node(node1, _attributes={
                    "shape": "doublecircle", "color": "black", "fontcolor": "black"})
        else:
            g2.node(str(node1))
            g2.node(node1, _attributes={"shape": "circle"})

        for node2 in G[node1]:
            if nodesAutomata[node2] == True:
                g2.node(node2, _attributes={
                        "shape": "doublecircle", "color": "black", "fontcolor": "black"})
            else:
                g2.node(str(node2))
                g2.node(node2, _attributes={"shape": "circle"})
            g2.edge(str(node1), str(node2), label=G[node1][node2])
    filename = g2.render(filename='graphs/automatas/' + nombre_archivo)


def delete_limboState(AFN, startNode, new_nodes_automata):
    color = {}
    for v in new_nodes_automata:
        color[v] = 'white'
    color[startNode] = 'gray'
    nodelist = [startNode]
    while nodelist != []:
        u = nodelist.pop()
        for neighbor in AFN[u]:
            if color[neighbor] == 'white':
                color[neighbor] = 'gray'
                if neighbor in AFN:
                    nodelist.append(neighbor)
        color[u] = 'black'
    for state in color:
        if color[state] == "white":
            del AFN[state]
            del new_nodes_automata[state]
    return AFN


def make_AFD(AFN, startNode, nodesAutomata, alphabet, id_ER):
    AFD = {}
    newStates = {}
    num_state = 0
    nodes = list(nodesAutomata.keys())
    while nodes != []:
        node = nodes.pop(0)
        for symbol in alphabet:
            state = {}
            isNew = True
            if node in AFN:
                for node2 in AFN[node].keys():
                    if symbol in AFN[node][node2]:
                        state[node2] = 0
            else:
                for newState in newStates:
                    for oldState in newStates[newState]:
                        for node2 in AFN[oldState].keys():
                            if symbol in AFN[oldState][node2]:
                                state[node2] = 0
            if len(state) > 1:
                for newState in newStates:
                    if newStates[newState] == state:
                        make_link_AFN(AFD, node, newState, symbol)
                        isNew = False
                        break
                if isNew:
                    nameState = "q" + str(num_state)
                    while nameState in nodesAutomata.keys():
                        num_state += 1
                        nameState = "q" + str(num_state)
                    num_state += 1
                    newStates[nameState] = state
                    make_link_AFN(AFD, node, nameState, symbol)
                    nodes.append(nameState)
            else:
                make_link_AFN(AFD, node, list(state.keys())[0], symbol)
    for newState in newStates:
        for oldState in newStates[newState]:
            if nodesAutomata[oldState]:
                make_state(nodesAutomata, True, newState)
            else:
                make_state(nodesAutomata, False, newState)

    delete_limboState(AFD, "q" + str(startNode), nodesAutomata)
    # drawAFN(AFD, startNode, nodesAutomata, "AFD_" + id_ER)
    return AFD


def add_lambda_closure(lambda_closures, initial_state, neighbor):
    if initial_state in lambda_closures:
        lambda_closures[initial_state].append(neighbor)
    else:
        lambda_closures[initial_state] = [neighbor]
    return lambda_closures


def find_lambda_closure(AFN, lambda_closures, AFN_e, startNode, nodesAutomata, new_nodes_automata):
    color = {}
    for v in nodesAutomata:
        color[v] = 'white'
    color[startNode] = 'gray'
    nodelist = [startNode]
    while nodelist != []:
        u = nodelist.pop()
        for neighbor in AFN_e[u]:
            if color[neighbor] == 'white':
                color[neighbor] = 'gray'
            if AFN_e[u][neighbor] == 'lambda':
                lambda_closures = add_lambda_closure(
                    lambda_closures, startNode, neighbor)
                if nodesAutomata[neighbor]:
                    nodesAutomata[u] = nodesAutomata[neighbor]
                if neighbor in AFN_e:
                    nodelist.append(neighbor)
            else:
                if u not in AFN:
                    AFN = make_link_AFN(AFN, u, neighbor, AFN_e[u][neighbor])
                elif neighbor not in AFN[u]:
                    AFN = make_link_AFN(AFN, u, neighbor, AFN_e[u][neighbor])
                elif AFN_e[u][neighbor] not in AFN[u][neighbor]:
                    AFN = make_link_AFN(AFN, u, neighbor, AFN_e[u][neighbor])
                new_nodes_automata[u] = nodesAutomata[u]
                new_nodes_automata[neighbor] = nodesAutomata[neighbor]
        color[u] = 'black'
    return lambda_closures, AFN, new_nodes_automata


def delete_lambda_transitions(lambda_closures, AFN, alphabet, nodesAutomata, new_nodes_automata):
    for state in lambda_closures:
        for state_neighbor in lambda_closures[state]:
            if state_neighbor in AFN:
                for neighbor in AFN[state_neighbor]:
                    for neighbor_transition in AFN[state_neighbor][neighbor]:
                        for symbol in alphabet:
                            if neighbor_transition == symbol:
                                if state not in AFN:
                                    AFN = make_link_AFN(
                                        AFN, state, neighbor, symbol)
                                elif neighbor not in AFN[state]:
                                    AFN = make_link_AFN(
                                        AFN, state, neighbor, symbol)
                                elif symbol not in AFN[state][neighbor]:
                                    AFN = make_link_AFN(
                                        AFN, state, neighbor, symbol)
                                new_nodes_automata[state] = nodesAutomata[state]
                                new_nodes_automata[neighbor] = nodesAutomata[neighbor]

    return AFN, new_nodes_automata


def make_AFN(AFN_e, startState, nodesAutomata, alphabet, id_ER):
    new_nodes_automata = {}
    AFN = {}
    lambda_closures = {}
    for node in AFN_e.keys():
        lambda_closures, AFN, new_nodes_automata = find_lambda_closure(AFN,
                                                                       lambda_closures, AFN_e, node, nodesAutomata, new_nodes_automata)
    AFN, new_nodes_automata = delete_lambda_transitions(
        lambda_closures, AFN, alphabet, nodesAutomata, new_nodes_automata)
    delete_limboState(AFN, "q" + str(startState), new_nodes_automata)
    # drawAFN(AFN, startState, new_nodes_automata, "AFN_" + id_ER)
    return AFN, new_nodes_automata


def start_end_states(Tree, node):
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

    del Tree[node]
    del Tree[node1]
    del Tree[node2]

    return startNode1, endNodes1, startNode2, endNodes2


def transition_concatenation(AFN_e, Tree, node, nodesAutomata, state, startState):
    startNode1, endNodes1, startNode2, endNodes2 = start_end_states(
        Tree, node)
    for endNode in endNodes1:
        nodesAutomata[endNode] = False
        AFN_e = make_link_AFNe(AFN_e, endNode, startNode2, "lambda")

    if nodesAutomata[startNode1] == True:
        AFN_e = make_link_AFNe(AFN_e, startNode1, startNode2, "lambda")

    if nodesAutomata[startNode2] == True:
        endNodes2.append(startNode2)

    nodesAutomata[startNode1] = False

    Tree = make_link_tree(Tree, node, "start", startNode1)
    Tree = make_link_tree(Tree, node, "end", endNodes2)

    startState = startNode1.split('q')[1]

    return AFN_e, Tree, nodesAutomata, state, startState


def transition_or(AFN_e, Tree, node, nodesAutomata, state, startState):
    startNode1, endNodes1, startNode2, endNodes2 = start_end_states(
        Tree, node)

    startNode = "q" + str(state)

    nodesAutomata = make_state(nodesAutomata, False, startNode)
    AFN_e = make_link_AFNe(AFN_e, startNode, startNode1, "lambda")
    AFN_e = make_link_AFNe(AFN_e, startNode, startNode2, "lambda")

    endNodes = endNodes1 + endNodes2
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes)

    startState = state
    state += 1
    return AFN_e, Tree, nodesAutomata, state, startState


def transition_kleen(AFN_e, Tree, node, nodesAutomata, state, startState):
    sub_node = list(Tree[node].keys())[0]
    endStates = []
    if type(sub_node) == str:
        AFN_e, Tree, nodesAutomata, state = transition(
            AFN_e, Tree, node, nodesAutomata, state)
        startState = Tree[node]['start']
        endStates = Tree[node]['end']
    else:
        startState = Tree[sub_node]['start']
        endStates = Tree[sub_node]['end']
        del Tree[sub_node]

    nodesAutomata[startState] = True
    for end_state in endStates:
        nodesAutomata[end_state] = True
        AFN_e = make_link_AFNe(AFN_e, end_state, startState, 'lambda')

    del Tree[node]
    endStates.append(startState)
    Tree = make_link_tree(Tree, node, 'start', startState)
    Tree = make_link_tree(Tree, node, 'end', endStates)

    startState = startState.strip('q')
    return AFN_e, Tree, nodesAutomata, state, startState


def transition_super(AFN_e, Tree, node, nodesAutomata, state, startState):
    sub_node = list(Tree[node].keys())[0]
    endStates = []
    if type(sub_node) == str:
        AFN_e, Tree, nodesAutomata, state = transition(
            AFN_e, Tree, node, nodesAutomata, state)
        startState = Tree[node]['start']
        endStates = Tree[node]['end']
    else:
        startState = Tree[sub_node]['start']
        endStates = Tree[sub_node]['end']
        del Tree[sub_node]

    nodesAutomata[startState] = False
    for end_state in endStates:
        nodesAutomata[end_state] = True
        AFN_e = make_link_AFNe(AFN_e, end_state, startState, 'lambda')

    del Tree[node]
    Tree = make_link_tree(Tree, node, 'start', startState)
    Tree = make_link_tree(Tree, node, 'end', endStates)

    startState = startState.strip('q')
    return AFN_e, Tree, nodesAutomata, state, startState


def transition(AFN_e, Tree, node, nodesAutomata, state):
    token = list(Tree[node].keys())[0]

    startState = "q" + str(state)
    endState = "q" + str(state + 1)
    AFN_e = make_link_AFNe(AFN_e, startState, endState, token)

    nodesAutomata = make_state(nodesAutomata, False, startState)
    nodesAutomata = make_state(nodesAutomata, True, endState)

    del Tree[node]
    startNode = startState
    endNodes = [endState]
    Tree = make_link_tree(Tree, node, "start", startNode)
    Tree = make_link_tree(Tree, node, "end", endNodes)

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


def makeAutomata(ERs):
    AFDS = {}
    ids_token = list(ERs.keys())
    for id_ER in ERs.keys():
        ER = ERs[id_ER]
        Tree, alphabet, compoused_automata = package.Parse_Tree.parseTree(ER, id_ER, ids_token)
        AFN_e = {}
        nodesAutomata = {}

        state = 0
        startState = 0

        len_tree = len(Tree)
        node_tree = 1
        while node_tree <= len_tree:
            subtree = Tree[node_tree]
            if len(subtree) == 1:
                AFN_e, Tree, nodesAutomata, state = transition(
                    AFN_e, Tree, node_tree, nodesAutomata, state)
            else:
                AFN_e, Tree, nodesAutomata, state, startState = select_transition(AFN_e, Tree, node_tree, nodesAutomata, state,
                                                                                  startState)
            node_tree += 1

        #drawAFNe(AFN_e, startState, nodesAutomata, "AFN-e_" + id_ER)
        AFN, nodesAutomata = make_AFN(
            AFN_e, startState, nodesAutomata, alphabet, id_ER)
        #AFD = make_AFD(AFN, startState, nodesAutomata, alphabet, id_ER)

        AFDS[id_ER] = [AFN, startState, nodesAutomata, compoused_automata]

    return AFDS
