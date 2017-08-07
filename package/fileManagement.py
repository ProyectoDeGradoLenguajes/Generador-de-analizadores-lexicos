# -*- coding: utf-8 -*-

import sys
import re


def open_File():
    name_file = sys.argv[1]
    file = open(name_file, encoding="utf8")
    return file


def close_file(file):
    file.close()


def create_file():
    file = open("../Analizer.py", "w")
    return file


def analizer_Code():
    code = """
def automata_Search(AFD, startState, nodesAutomata, word):
    isAcepted = False
    nextState = startState
    for symbol in word:
        state = nextState
        found = False
        for neighbor in AFD[state]:
            labels = AFD[state][neighbor]
            for label in labels:
                if label == symbol:
                    nextState = neighbor
                    found = True
                    break
        if not found:
            return isAcepted

    if nodesAutomata[nextState]:
        isAcepted = True
    return isAcepted


def main():
    AFD = {'q2': {'q2': ['b'], 'q4': ['c'], 'q0': ['a']}, 'q7': {'q2': ['b'], 'q4': ['c'], 'q0': [
        'a']}, 'q0': {'q2': ['b'], 'q4': ['c'], 'q0': ['a']}, 'q4': {'q2': ['b'], 'q4': ['c'], 'q0': ['a']}}
    startState = 'q7'
    nodesAutomata = {'q2': True, 'q7': True, 'q0': True, 'q4': True}

    word = sys.stdin.readline().strip('\n')
    word = list(map(str, word))

    result = automata_Search(AFD, startState, nodesAutomata, word)
    print(result)

main()
"""
    return code
def generate_Code():
    file_input = open_File()
    file_output = create_file()
    file_output.write("import sys")

    counter = 0
    for line in file_input:
        if line != "(O_O¬)\n" and counter == 1:
            file_output.write(line)
        elif line != "(O_O¬)\n" and counter == 2:
            line = line.strip('\n')
            line = re.split('[\s]+', line)
        elif line != "(O_O¬)\n" and counter == 3:
            file_output.write(line)
        else:
            counter += 1
    file_output.write(analizer_Code())

    file_input.close()
    file_output.close()

generate_Code()
