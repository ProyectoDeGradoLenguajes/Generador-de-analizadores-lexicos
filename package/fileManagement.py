import sys
#Read the input file structure
def readStructure(ifile, ofile, token):
    inputFile = open(ifile, 'r')
    if (inputFile.readline().strip() != token):
        sys.error("Incorrect token in start")
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

#Opera segunda seccion
def analizerSection(outputFile, inputFile, token):
    line = inputFile.readline().strip()
    while(line != token):
        outputFile.write("sexy\n")
        line = inputFile.readline().strip()
    pass

