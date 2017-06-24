def makeTree(ER):
    binary_operations = {'|': op_OR,
                         ')': parenthesis_Close, '(': parenthesis_Open}
    unary_operations = {'*': op_KleenStar, '+': op_SuperPlus}
    Parenthesis_dic = {}

    for character in ER 
    
def arbolSignificado(fileER):
    #fileER = open('test/prueba.txt', 'r')
    for ER in fileER:
        # print "caso --->", i + 1
        ER.strip()
        ER = list(map(str, ER))
        # ER almacenara una lista con el orden en que deben ser operados los
        # parentesis
        final_tree = makeTree(ER)

        drawTree(final_tree, "finals")
        return final_tree

print(arbolSignificado(["(x*y(b|d)+as*)+"]))