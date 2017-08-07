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
        
        outputFile.write(line + '\n')
    outputFile.close()
    return
