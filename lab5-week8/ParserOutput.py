

from typing import List
from Parser import Parser


class ParserOutput:
    def __init__(self, fileName, pifFileName) -> None:
        self.parser = Parser(fileName)
        self.parser.CanonicalCollection()
        self.parser.createTable()
        #this will be a file with rows of form: symbol value
        self.pifFile = pifFileName
        self.returnedMessage = ""
        self.returnedOutput = ""


    def parsePif(self):
        fullArray = []
        with open(self.pifFile) as file:
            allLines = file.readlines()
            for line in allLines:
                fullArray.append(line.split()[0])

        return self.parse(fullArray)

    def shift(self, builtPath,inputStringArray,output):
        firstChar = inputStringArray.pop(0)
        firstCharPositionInTabel = self.parser.allCharacters.index(firstChar)
        nextSetNumber = self.parser.table[builtPath[-1]][1][firstCharPositionInTabel]
        builtPath.append(firstChar)
        builtPath.append(nextSetNumber)

    def createArrayFromPath(self,builtPath,inputStringArray,output):
        newOutput = []
        for element in builtPath:
            if isinstance(element,str):
                newOutput.append(element)
        for element in inputStringArray:
            if isinstance(element,str):
                newOutput.append(element)
        output.insert(0,newOutput)

    def reduce(self, reduceCommand:str,builtPath,inputStringArray,output):
        productionNumber = int(reduceCommand.strip().split()[1])
        production = self.parser.numberedProductions[productionNumber]
        productionNonTerminal = production[0]
        productionArray = production[1]
        for character in productionArray[::-1]:
            if character == "~":
                continue
            builtPath.pop()
            removedCharacter = builtPath.pop()
            if removedCharacter != character:
                builtPath.append(-1)
                output = ["error at reduce, at production " + str(production) + ", " + removedCharacter + " is not equal to character in production " + character]
                return
        builtPath.append(productionNonTerminal)
        firstCharPositionInTable = self.parser.allCharacters.index(productionNonTerminal)
        nextSetNumber = self.parser.table[builtPath[-2]][1][firstCharPositionInTable]
        builtPath.append(nextSetNumber)

    def parse(self, inputStringArray):
        #alpha = builtPath
        #beta = inputString
        #phi = output
        currentStateIndex = 0
        builtPath = [0]
        returnedMessage = "error"
        output = [inputStringArray.copy()]
        done = False
        while not done:
            if self.parser.table[currentStateIndex][0] == "shift":
                self.shift(builtPath,inputStringArray,output)
                currentStateIndex = builtPath[-1]
            elif currentStateIndex > -1 and "reduce" in self.parser.table[currentStateIndex][0]:
                self.reduce(self.parser.table[currentStateIndex][0],builtPath,inputStringArray,output)
                currentStateIndex = builtPath[-1]
                if currentStateIndex != -1:
                    self.createArrayFromPath(builtPath,inputStringArray,output)
            else:
                if currentStateIndex > -1 and self.parser.table[currentStateIndex][0] == "accept":
                    returnedMessage = "success"
                    done = True
            if currentStateIndex == -1:
                done = True
        self.returnedOutput = output
        self.returnedMessage = returnedMessage
        return (returnedMessage,output)
    def writeOutput(self):
        with open("OUT.out", "w+") as handler:
            handler.write(self.returnedMessage+'\n')
            for output in self.returnedOutput:
                handler.write(str(output)+'\n')


a = ParserOutput("works.txt", "seq.txt")
a.parsePif()
a.writeOutput()
#print(a.parse(["a","b","c","d","a"]))