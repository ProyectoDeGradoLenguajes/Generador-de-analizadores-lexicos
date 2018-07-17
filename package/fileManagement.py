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


def analizer_Code(file, AFDs, Functions, newFunctions, new_mainLines):
    for function in Functions.keys():
        file.write("\n \n" + Functions[function][0])

    file.write(""" 
def mmult(A,B):
    AB = [[0 for k in range(len(B[0]))] for j in range(len(A))]
    for i,row in enumerate(A):
        for j,col in enumerate([list(c) for c in zip(*B)]):
            AB[i][j] = sum([a*b for a,b in zip(row,col)])
    return AB

def markovMatrix(matrixes): 
    hola_meaning = [[13.78,28.74,28.74,28.74,28.74],[24.9433,25.17,24.9433,24.9433],[24.9167,24.9167,25.25,24.9167],[21.4,21.4,21.4,35.8]]
    matrix_initial = [hola_meaning]
    if len(matrixes) == 0:
        for matrix in matrix_initial:
            matrixes.append(mmult(matrix,matrix))
    else:
        matrixes_new = []
        for i in range(len(matrixes)):
            matrixes_new.append(mmult(matrixes[i],matrix_initial[i]))
        matrixes = matrixes_new[:]
    return matrixes

def printMarkov(dicYAFP, matrixes):
    listYAFP = list(dicYAFP.keys())
    toString = ""
    i = 1
    j = 0
    for matrix in matrixes:
        if i == 1:
            toString =  toString + "\\n" + listYAFP[j] + "_meaning :"
            j+=1
            i-=1            
        for i in range(len(matrix)):
            toString = toString + str(matrix[i][i]/100) + " ,"
    print(toString)

def compoused_automata_Search(AFD, startState, nodesAutomata, word, AFDS, start_states, nodes_automatas):
    isAcepted = False
    nextState = startState
    count = 0
    for symbol in word:
        state = nextState
        found = False
        for neighbor in AFD[state]:
            labels = AFD[state][neighbor]
            for label in labels:
                if label in AFDS:
                    sub_automata = automata_Search(
                        AFDS[label], start_states[label], nodes_automatas[label], symbol)
                    if sub_automata:
                        count += 1
                        found = True
                    elif not sub_automata and count > 0:
                        nextState = neighbor
                        found = True
                        count = 0
                elif label == symbol:
                    nextState = neighbor
                    found = True
                    break

        if not found:
            return isAcepted

    if nodesAutomata[nextState]:
        isAcepted = True
    return isAcepted


def automata_Search(AFD, startState, nodesAutomata, word):
    numbers = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight",
               "9": "nine", "0": "zero"}
    isAcepted = False
    nextState = startState
    for symbol in word:
        if symbol in numbers:
            symbol = numbers[symbol]
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
    nlp = spacy.load('es')
    unrecognized = []          
"""
               )
    completeAFD = ''
    start_states = ''
    nodes = ''
    completeCompoused = ''
    dic_functions = ''
    verb_dic_functions = ''

    for id_AFD in Functions.keys():

        if id_AFD in AFDs.keys():
            AFD = AFDs[id_AFD][0]
            startState = AFDs[id_AFD][1]
            nodesAutomata = AFDs[id_AFD][2]
            compoused_automata = AFDs[id_AFD][3]

            id_name = "AFD_" + id_AFD
            file.write("    " + id_name + " = " + str(AFD) + "\n")
            if completeAFD == '':
                completeAFD = "'" + id_AFD + "'" + " : " + id_name
            else:
                completeAFD = completeAFD + "," + "'" + id_AFD + "'" + " : " + id_name

            id_startstate = "startState_" + id_AFD
            file.write("    " + id_startstate +
                       " = 'q" + str(startState) + "'\n")
            if start_states == '':
                start_states = "'" + id_AFD + "'" + " : " + id_startstate
            else:
                start_states = start_states + "," + "'" + id_AFD + "'" + " : " + id_startstate

            id_nodes = "nodesAutomata_" + id_AFD
            file.write("    " + id_nodes + " = " + str(nodesAutomata) + "\n")
            if nodes == '':
                nodes = "'" + id_AFD + "'" + " : " + id_nodes
            else:
                nodes = nodes + "," + "'" + id_AFD + "'" + " : " + id_nodes

            id_compoused = "compoused_" + id_AFD
            file.write("    " + id_compoused + " = " +
                       str(compoused_automata) + "\n\n")
            if completeCompoused == '':
                completeCompoused = "'" + id_AFD + "'" + " : " + id_compoused
            else:
                completeCompoused = completeCompoused + "," + \
                    "'" + id_AFD + "'" + " : " + id_compoused

            if Functions[id_AFD][1] == 2:
                if dic_functions == '':
                    dic_functions = "'" + id_AFD + "'" + " : " + id_AFD
                else:
                    dic_functions = dic_functions + "," + "'" + id_AFD + "'" + " : " + id_AFD
        elif Functions[id_AFD][1] == 4:
            if verb_dic_functions == '':
                verb_dic_functions = "'" + id_AFD + "'" + " : " + id_AFD
            else:
                verb_dic_functions = verb_dic_functions + \
                    "," + "'" + id_AFD + "'" + " : " + id_AFD

    file.write("    AFDS = {" + str(completeAFD) + "}\n")
    file.write("    start_states = {" + str(start_states) + "}\n")
    file.write("    nodes_automatas = {" + str(nodes) + "}\n")
    file.write("    is_compoused = {" + str(completeCompoused) + "}\n")
    file.write("    functions = {" + str(dic_functions) + "}\n")
    file.write("    VERB_functions = {" + str(verb_dic_functions) + "}\n")
    if len(new_mainLines) > 0:
        for newLine in new_mainLines:
            file.write("\n")
            file.write(newLine)
    else:
        file.write("""
    sentences = [sys.stdin.readline().strip('\\n')]
            """)
    file.write("""
    matrixes = []
    dictionaryYAFP = {"mujer":0}
    for sentence in sentences:
        words = sentence.split(' ')   
        for word in words:
            result = False
            for id_AFD in AFDS.keys():
                AFD = AFDS[id_AFD]
                startState = start_states[id_AFD]
                nodesAutomata = nodes_automatas[id_AFD]
                if is_compoused[id_AFD]:
                    result = compoused_automata_Search(
                        AFD, startState, nodesAutomata, word, AFDS, start_states, nodes_automatas)
                else:
                    result = automata_Search(AFD, startState, nodesAutomata, word)
                if result:
                    if word in dictionaryYAFP:
                        matrixes = markovMatrix(matrixes)[:]
                    doc = nlp(word)
                    for w in doc:
                        is_conjugated=False
                        for function in VERB_functions.keys():
                            if VERB_functions[function](word):
                                is_conjugated = True
                                break
                        if not is_conjugated and w.pos_ == "VERB":
                            print("<<", word, ">> => es un verbo")                                    
                        else:                            
                            functions[id_AFD](word)
                    break
            if not result:
                unrecognized.append(word)
    print(\" No se reconocio dentro del lenguaje, los siguientes caracteres:\\n \", unrecognized)
    printMarkov(dictionaryYAFP, matrixes)\n""")
    for newfunction in newFunctions:
        file.write('    ' + newfunction + "\n")
    if len(new_mainLines) > 0:
        file.write("main()")
    else:
        file.write("""
while True:
    main()""")


def separate_line(line):
    line.strip(' ')
    line.strip('\n')
    is_er = False
    is_function = False
    is_name = True
    name = ''
    er = ''
    function = ''
    for character in line:
        if character == ':':
            is_er = True
            is_name = False
        elif character == '{':
            is_er = False
            is_function = True
        elif is_name:
            name = name + character
        elif is_er:
            er = er + character
        elif is_function and character != '}':
            function = function + character

    newline = []
    newline.append(name)
    newline.append(er)
    newline.append(function)
    return newline


def generate_Code(name_file):
    token = "(O_O¬)\n"

    file_input = open_File(name_file)
    if file_input.readline() != token:
        file_input.close()
        print("The file should start with " + token)
        return

    file_output = create_file()
    file_output.write("import sys \nimport spacy \nimport re \n")
    ERs = {}
    Functions = {}
    newFunctions = []
    areMainLines = False
    main_newLines = []

    counter = 0
    for line in file_input:
        if line != token and counter == 1:
            file_output.write(line)
        elif line != token and counter == 2:
            line = separate_line(line)[:]
            ERs[line[0]] = line[1]
            nameFunction = line[0]
            function = "def " + nameFunction + "(word):\n     " + line[2]
            Functions[nameFunction] = [function, counter]
        elif line != token and counter == 3:
            if 'main' in line and not areMainLines:
                areMainLines = True
            elif "def" in line:
                areMainLines = False
                thisLine = re.split('[\s]+', line)
                newFunctions.append(thisLine[1].strip(":"))
                file_output.write(line)
            elif areMainLines:
                main_newLines.append(line)
            else:
                file_output.write(line)
        elif line != token and counter == 4:
            line = separate_line(line)[:]
            nameFunction = line[0]
            function = "def " + nameFunction + \
                "(word):\n\t" + "if re.search(\'" + \
                line[1] + "\', word):\n\t" + \
                "\tprint(\"<<\", word, \">> => es un verbo en " + nameFunction + \
                "\")\n\t\t" + line[2] + \
                "\t\treturn True" + "\n\treturn False"
            Functions[nameFunction] = [function, counter]
        else:
            counter += 1

    if counter < 2:

        file_input.close()
        file_output.close()
        os.remove("Analyzer.py")
        print("The file does not contain regular expressions")
        return

    AFDs = package.Automata.makeAutomata(ERs)
    analizer_Code(file_output, AFDs, Functions, newFunctions, main_newLines)

    file_input.close()
    file_output.close()
