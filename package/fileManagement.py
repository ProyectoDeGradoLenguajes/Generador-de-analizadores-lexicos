import sys
import re
#Read the input file structure
def readStructure(ifile, ofile, token):
    inputFile = open(ifile, 'r')
    if (inputFile.readline().strip() != token):
        sys.error("The file should start with " + token)
    else:
        copySection(ofile, inputFile, token)

#Copy and paste code in first and third section in the output file
def copySection(ofile, inputFile, token):
    counter = 0
    outputFile = open(ofile, 'w')
    for line in inputFile:
        line = line.strip()
        if (line == token):
            analizerSection(outputFile, inputFile, token)
            continue
        outputFile.write(line + '\n')
    outputFile.close()
    return

#Takes the second section, create his automaton and link it with the corresponding functions
def analizerSection(outputFile, inputFile, token):
    line = inputFile.readline().strip()
    while(line != token):
        line = re.split('[\s]+', line)
        for i in line:
            print(i)
        outputFile.write(line[0] + " " + line[1] + " " + line[2] + "\n")
        line = inputFile.readline().strip()
    pass

