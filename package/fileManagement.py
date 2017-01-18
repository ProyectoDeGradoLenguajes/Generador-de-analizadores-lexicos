import sys
#Read the input file structure
def readStructure(ifile, ofile, token):
    counter = 0
    inputFile = open(ifile, 'r')
    for line in inputFile:
        line = line.strip()
        if (line == token):
            counter += 1
        if( counter%2 != 0):
            copySection(ofile, line)
        else:
            analizerSection(line)

#Copy and paste code in first and third section in the output file
def copySection(ofile, line):
    outputFile = open(ofile, 'a')
    outputFile.write(line)
    outputFile.close()
    return

#Opera segunda seccion
def analizerSection(line):
    pass

