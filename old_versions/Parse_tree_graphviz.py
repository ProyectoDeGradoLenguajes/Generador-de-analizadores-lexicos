import graphviz as graph
import sys


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
    filename = g2.render(filename='graphs/parse_tree/g' + etiqueta)


def op_unary(tree, character, node, pair):
    prev_node = node - 1
    if len(tree[prev_node]) >= 2:
        make_link(tree, prev_node - 1, character)
    else:
        make_link(tree, prev_node, character)
    return tree, node, pair


def op_OR(tree, node, character, position_or, pair):
    pair = []
    prev_node = node - 1
    if len(position_or) == 0 and character == '|':
        position_or.append(prev_node)
    else:
        make_link(tree, node, '|')
        make_link(tree, node, position_or.pop())
        make_link(tree, node, prev_node)
        if character == '|':
            position_or.append(node)
        else:
            pair.append(node)
        node += 1

    return tree, node, position_or, pair


def op_concatenation(tree, character, node, pair):
    tree = make_link(tree, node, character)
    pair.append(node)

    if len(pair) == 2:
        node += 1
        node1 = pair.pop()
        node2 = pair.pop()
        tree = make_link(tree, node, node1)
        tree = make_link(tree, node, node2)
        pair.append(node)
    node += 1
    return tree, node, pair


def makeSubTree(tree, sub_ER, node):
    unary_operations = {'*': op_unary, '+': op_unary, "$": 0, "/": 0, "?": 0}
    pair = []
    position_or = []

    i = 1
    while i < len(sub_ER):
        character = sub_ER[i]
        if character == '|' or (character == ')' and len(position_or) > 0):
            tree, node, position_or, pair = op_OR(
                tree, node, character, position_or, pair)
        elif character in unary_operations:
            tree, node, pair = unary_operations[character](
                tree, character, node, pair)
        elif character != ')':
            tree, node, pair = op_concatenation(
                tree, character, node, pair)
        i += 1
    return tree, node


def makeTree(ER):
    numbers = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight",
               "9": "nine", "0": "zero"}
    operations = {"*": 0, "|": 0, "+": 0,
                  "(": 0, ")": 0, "/": 0, "?": 0, ".": 0}

    tree = {}
    alphabet = []
    node = 1
    parenthesis_position = []

    i = 0
    while i < len(ER):
        character = ER[i]

        if character.isdigit():
            ER[i] = numbers[character]

        if ER[i] not in alphabet and character not in operations:
            alphabet.append(ER[i])

        if character == '(':
            parenthesis_position.append(i)

        if character == ')':
            parenthesis = parenthesis_position.pop()
            sub_ER = ER[parenthesis:(i + 1)]
            tree, node = makeSubTree(tree, sub_ER, node)
            del ER[parenthesis:(i + 1)]
            ER.insert(parenthesis, node - 1)
            i = parenthesis
        i += 1
    return tree, alphabet


def metaCharacters(ER):
    search = True
    while search:
        if ER.find("[") > 0 and ER.find("]") > 0:
            subER = ER[ER.find("[") + 1: ER.find("]")]
            newSubER = groupCharacters(subER)
            ER = ER.replace("[" + subER + "]", newSubER)
        else:
            search = False
    return ER


def groupCharacters(subER):
    newSubER = ''
    for i in range(0, len(subER)):
        character = subER[i]
        if character == '-':
            i -= 1
            character1 = subER[i]
            asciiCharacter1 = ord(character1) + 1
            i += 2
            character2 = subER[i]
            asciiCharacter2 = ord(character2)
            for j in range(asciiCharacter1, asciiCharacter2):
                newSubER = newSubER + chr(j) + "|"
        else:
            newSubER = newSubER + character + "|"
    finalStep = len(newSubER) - 1
    newSubER = newSubER[:finalStep]
    return "(" + newSubER + ")"


def deleteMetaCharacters(ER):
    i = 0
    while i < len(ER):
        character = ER[i]
        if character == "^" or character == "$":
            ER.pop(i)
        i += 1
    return ER


def separateTokens(ER, ids_token):
    for id_token in ids_token:
        location = str(ids_token.index(id_token))
        ER = ER.replace(id_token, location)
    ER = list(map(str, ER))
    i = 0
    while i < len(ER):
        token = ER[i]
        if token.isdigit():
            ER.pop(i)
            ER.insert(i, ids_token[int(token)])
        i += 1
    return ER


def parseTree(ER, id_ER, ids_token):
    ER = "(" + ER + ")"
    ER = metaCharacters(ER)
    ER_with_ids = False

    for id_token in ids_token:
        if id_token in ER:
            ER_with_ids = True
            break

    if ER_with_ids:
        ER = separateTokens(ER, ids_token)
    else:
        ER = list(map(str, ER))

    ER = deleteMetaCharacters(ER)
    final_tree, alphabet = makeTree(ER)
    drawTree(final_tree, "_" + id_ER)
    return final_tree, alphabet, ER_with_ids
