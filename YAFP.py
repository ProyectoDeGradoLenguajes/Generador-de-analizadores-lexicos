"""
Main of the proyect
All the creation of objects and his interaction should be created here
Other files contains modules in their respective folders
"""
import sys
import package.fileManagement

def YAFP():
    name_file = sys.argv[1]
    package.fileManagement.generate_Code(name_file)

YAFP()
    