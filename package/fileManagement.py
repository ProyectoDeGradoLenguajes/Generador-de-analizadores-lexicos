import sys
import re
import package.Automata
import os


def open_File(name_file):
    file = open(name_file, encoding="utf8")
    return file


def close_file(file):
    file.close()


def create_file():
    file = open("Analyzer.py", "w")
    return file


def analizer_Code(file, AFD, startState, nodesAutomata, Functions, newFunctions):
    for function in Functions.keys():
        file.write("\n \n" + Functions[function])

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

    if result:
""")
    for function in Functions.keys():
        file.write("        " + function + "\n")

    file.write("""
    else:
        print(result)

""")
    for function in newFunctions:
        file.write("    " + function + "\n")
    
    file.write("""
while True:
    main()
""")


def generate_Code(name_file):
    token = "(O_O¬)\n"

    file_input = open_File(name_file)
    if file_input.readline() != token:
        file_input.close()
        print("The file should start with " + token)
        return

    file_output = create_file()
    file_output.write("import sys \n")
    ERs = []
    Functions = {}
    newFunctions = []
    countFuntions = 0

    counter = 0
    for line in file_input:
        if line != token and counter == 1:
            file_output.write(line)
        elif line != token and counter == 2:
            line = line.strip('\n')
            line = re.split('[\s]+', line)
            if len(line) == 3:
                ERs.append(line[1])
                nameFunction = line[0] + "_Print()"
                function = "def " + nameFunction + ":\n     " + line[2]
                Functions[nameFunction] = function
            else:
                ERs.append(line[0])
                nameFunction = "id" + str(countFuntions) + "_Print()"
                function = "def " + nameFunction + ":\n     " + line[1]
                Functions[nameFunction] = function
        elif line != token and counter == 3:
            if "def" in line:
                thisLine = re.split('[\s]+', line)
                newFunctions.append(thisLine[1].strip(":"))
            file_output.write(line)
        else:
            counter += 1

    if counter < 2:
        
        file_input.close()
        file_output.close()
        os.remove("Analyzer.py")
        print("The file does not contain regular expressions")
        return

    AFD, startState, nodesAutomata = package.Automata.makeAutomata(ERs)
    analizer_Code(file_output, AFD, startState,
                  nodesAutomata, Functions, newFunctions)

    file_input.close()
    file_output.close()

