import sys
import graphviz as graph
import os


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


def op_unary(tree, node, node_aux, character):
    if len(tree[node_aux]) > 1:
        if "|" in tree[node_aux] and node_aux in tree[node - 1]:
            del tree[node - 1]
            tree = make_link(tree, node - 1, character)
            tree = make_link(tree, node - 1, node_aux)

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
    if (len(position_or) == 0):
        position_or.append(node - 1)
        pair = 0
    else:
        node1 = position_or.pop()
        node2 = node - 1
        tree = make_link(tree, node, node1)
        tree = make_link(tree, node, node2)
        tree = make_link(tree, node, '|')

        if character == '|':
            pair = 0
            position_or.append(node)
        else:
            pair = 1

        node += 1
    return tree, node, position_or, pair


def op_concatenation(tree, node, node1, node2, pair, character):
    flag = False
    if (character != ")"):
        if (type(character) is not int):
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
    unary_operations = {'*': op_unary, '+': op_unary, "$": 0, "/": 0, "?": 0}
    binary_operations = {'|': 1, ')': 1}
    pair = 0
    position_or = []

    sub_ER.pop(0)
    # print(sub_ER)
    i = 0
    while i < len(sub_ER):
        character = sub_ER[i]
        prev_character = sub_ER[i - 1]
        if type(prev_character) is int and sub_ER[i] in unary_operations:
            tree, node = op_unary(tree, node, prev_character - 1, character)
        elif type(character) is int:
            pair += 1
            if type(prev_character) is int:
                node1 = character - 1
                node2 = prev_character - 1
                tree, node, pair = op_concatenation(
                    tree, node, node1, node2, pair, character)
            else:
                node1 = node - 1
                node2 = character - 1
                tree, node, pair = op_concatenation(
                    tree, node, node1, node2, pair, character)

        elif type(character) is str:
            if character in unary_operations:
                tree, node = op_unary(tree, node, 0, character)
            elif character in binary_operations:
                tree, node, position_or, pair = op_OR(
                    tree, node, position_or, pair, character)
            else:
                node1 = node - 1
                node2 = node - 2
                tree, node, pair = op_concatenation(
                    tree, node, node1, node2, pair, character)
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

        if (character == "("):
            parenthesis_position.append(i)

        if (character == ")"):
            parenthesis = parenthesis_position.pop()
            sub_ER = ER[parenthesis:(i + 1)]
            tree, node = makeSubTree(tree, sub_ER, node)
            del ER[parenthesis:(i + 1)]
            ER.insert(parenthesis, node)
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


def parseTree(ER):
    ER = "(" + ER + ")"
    ER = metaCharacters(ER)
    ER = list(map(str, ER))
    ER = deleteMetaCharacters(ER)
    final_tree, alphabet = makeTree(ER)
    drawTree(final_tree, "final")
    return final_tree, alphabet


parseTree("a[0-9]z")
