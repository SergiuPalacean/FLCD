

class Grammar:
    nonterminals = []
    terminals = []
    startingSymbol = ""
    productions = {}
    inputFile = ""


    # def __init__(self,givenInputFile):
    #     self.inputFile = givenInputFile

    def readFile(self,givenInputFile):
        self.inputFile = givenInputFile
        lineNumber = 0
        with open(self.inputFile) as fileHandler:
            lines = fileHandler.readlines()
            for line in lines:
                line = line.strip()
                if lineNumber == 0:
                    self.nonterminals = line.split(" ")
                elif lineNumber == 1:
                    self.terminals = line.split(" ")
                elif lineNumber == 2:
                    self.startingSymbol = line
                else:
                    if line.strip() == "":
                        continue
                    # do we need to save spaces?
                    # A ~ a 1 B| c
                    parts = line.split("~")
                    parts[0] = parts[0].strip()
                    if parts[0] not in self.productions:
                        self.productions[parts[0]] = []
                    for individualProduction in parts[1].split("|"):
                        self.productions[parts[0]].append(individualProduction.strip().split(" "))
                lineNumber += 1

    
    #make raise an error
    def getProductionsForNonterminal(self,givenNonterminal):
        if givenNonterminal in self.productions:
            return self.productions[givenNonterminal]

    def CFGcheck(self):
        for leftSide in self.productions.keys():
            if leftSide not in self.nonterminals:
                return False
        return True

# a = Grammar()
# a.readFile("g2.txt")
#print(a.nonterminals)
#print(a.terminals)
#print(a.productions)
# for i in a.productions:
#     for ii in a.productions[i]:
#         if '' in ii:
            # print(ii)
#print(a.CFGcheck())


    