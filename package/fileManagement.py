import sys
import re
import Automata


def open_File():
    name_file = sys.argv[1]
    file = open(name_file, encoding="utf8")
    return file


def close_file(file):
    file.close()


def create_file():
    file = open("../Analyzer.py", "w")
    return file


def analizer_Code(file, AFD, startState, nodesAutomata):
    file.write(""" 

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
          
"""
               )
    file.write("    AFD = " + str(AFD) + "\n")
    file.write("    startState = 'q" + str(startState) + "'\n")

    file.write("    nodesAutomata = " + str(nodesAutomata) + "\n")
    file.write("""
    word = sys.stdin.readline().strip('\\n')
    word = list(map(str, word))

    result = automata_Search(AFD, startState, nodesAutomata, word)
    print(result)

main()
"""
               )


def generate_Code():
    file_input = open_File()
    file_output = create_file()
    file_output.write("import sys \n")
    ERs = []

    counter = 0
    for line in file_input:
        if line != "(O_O¬)\n" and counter == 1:
            file_output.write(line)
        elif line != "(O_O¬)\n" and counter == 2:
            line = line.strip('\n')
            line = re.split('[\s]+', line)
            ERs.append(line[0])
        elif line != "(O_O¬)\n" and counter == 3:
            file_output.write(line)
        else:
            counter += 1

    AFD, startState, nodesAutomata = Automata.makeAutomata(ERs)
    print(AFD.keys())
    print(nodesAutomata)
    analizer_Code(file_output, AFD, startState, nodesAutomata)

    file_input.close()
    file_output.close()


generate_Code()
