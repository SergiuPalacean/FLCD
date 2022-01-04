from copy import copy, deepcopy
from typing import final

from Grammar import Grammar


class Parser:
    def __init__(self,fileName) -> None:
        self.grammar = Grammar()
        self.grammar.readFile(fileName)
        #[[[],[]],[[]]]
        self.allSets = []
        #[[],[],[]]
        self.forCheckingAllSets = []
        self.table = []
        self.allCharacters = copy(self.grammar.nonterminals)
        self.allCharacters += copy(self.grammar.terminals)
        self.numberedProductions = []
        
    
    #[["S'",["~","S"]],[...]]
    #["~","S"].index("~")
    
    def closureRecursive(self,elementArray,returnedSet):

        pointIndex = elementArray.index("~")
        nonterminal = elementArray[pointIndex+1]
        currentSet = []

        elementsAdded = False
        #goes through all the productions of the nonterminal and adds them after putting ~ first
        for each in self.grammar.productions[nonterminal]:
            eachCopy = each.copy()
            eachCopy.insert(0,"~")
            addedElement = [nonterminal,eachCopy]
            #since we know we added ~ as the first element we know we have to check the second element if it is a nonterminal
            if eachCopy[1] in self.grammar.nonterminals:
                currentSet.append(eachCopy)
            #we we check to make sure the element is not already in the new set
            if addedElement not in returnedSet:
                elementsAdded = True
                returnedSet.append(addedElement)
            
        #we continue to add elements to the newSet
        if elementsAdded:
            for eachElement in currentSet:
                self.closureRecursive(eachElement,returnedSet)


    def checkNewSet(self,newSet):
        newElement = False
        for each in newSet:
            if each and each not in self.forCheckingAllSets:
                newElement = True
                break
        if newElement:
            self.allSets.append(newSet)
            self.forCheckingAllSets += newSet

    #param
    #set - -array of individualSets, of form ["S'",["~","S"]]
    #it does not return anything, it tries to create a new set
    def closure(self, set):
        newSet = []
        #create the new set
        for individualSet in set:
            #we get the parts of each individual set
            individualSetElement = individualSet[0]
            individualSetArray = individualSet[1]
            pointIndex = individualSetArray.index("~")

            #case where ~ is the last element, we add the individualSet to the new set we are creating and stop
            newSet.append(individualSet)
            if pointIndex + 1 != len(individualSetArray):
                if individualSetArray[pointIndex+1] in self.grammar.nonterminals:
                    self.closureRecursive(individualSetArray,newSet)
        
        #check if the new set has new elements
        self.checkNewSet(newSet)
    
                


    #params: 
    #set -array of individualSets, of form ["S'",["~","S"]]
    #element - a string
    #it should call closure(set*), where set* is the array of individualSets that had ~ before element and now have it after element 
    def goto(self,set,element):
        allCLosureArray = []
        #we get each pair element-production
        for individualSet in set:
            individualSetElement = individualSet[0]
            individualSetArray = individualSet[1]
            #get the position of the ~ (element we use as .)
            pointIndex = individualSetArray.index("~")
            if pointIndex +1 <len(individualSetArray) and individualSetArray[pointIndex+1] == element:
                #make a copy of the production and swap the element with the point
                closureArray = deepcopy(individualSetArray)
                closureArray[pointIndex], closureArray[pointIndex+1] = closureArray[pointIndex+1], closureArray[pointIndex]
                allCLosureArray.append([individualSetElement,closureArray])
        #print(allCLosureArray)
        self.closure(allCLosureArray)
        


    def CanonicalCollection(self):
        self.closure([[self.grammar.startingSymbol+"`",["~",self.grammar.startingSymbol]]])
        i = 0
        while i < len(self.allSets):
            for term in self.grammar.nonterminals:
                self.goto(self.allSets[i],term)
            for term in self.grammar.terminals:
                self.goto(self.allSets[i],term)
            i +=1
        #work with ~ in place of .

    def prettyPrintSets(self):
        i = 0
        for set in self.allSets:
            print("set" + str(i) + ": " +str(set))
            i+=1

    

    def checkAccept(self, setIndex):
        #return true or false
        finalSet = [self.grammar.startingSymbol+"`",[self.grammar.startingSymbol,"~"]]
        for individualSet in self.allSets[setIndex]:
            if individualSet == finalSet:
                return True
        return False

    def getShift(self,setIndex,char,previousPointIndex):
        #returns the set index for shiftself.table
        returnedValue = -2
        #TODO maybe change to setIndex + 1
        for i in range(setIndex+1,len(self.allSets)):
            for individualSet in self.allSets[i]:
                individualSetArray = individualSet[1]
                if char in individualSetArray:
                    # if individualSetArray.index(char) + 1 == individualSetArray.index("~"):
                    if individualSetArray[previousPointIndex] == char:
                        returnedValue = i
                        return returnedValue
        return returnedValue
    

    
    def createTable(self):
        #only use this for reduce, so we add ~ to the end to compare in an easier way
        errorSets = {}

        for key in self.grammar.productions.keys():
            for production in self.grammar.getProductionsForNonterminal(key):
                productionCopy = copy(production)
                productionCopy.append("~")
                self.numberedProductions.append([key,productionCopy])
        
        for currentSetIndex in range(len(self.allSets)):
            self.table.append([None,None])
            if self.checkAccept(currentSetIndex):
               self.table[currentSetIndex][0] = "accept"
            else:
                #check reduce
                for individualSet in self.allSets[currentSetIndex]:
                    if individualSet in self.numberedProductions:
                        if  self.table[currentSetIndex][0] == None:
                            productionNumber = self.numberedProductions.index(individualSet)
                            self.table[currentSetIndex][0] = "reduce "+ str(productionNumber)
                            self.table[currentSetIndex][1] = productionNumber
                        else :
                            if currentSetIndex not in errorSets:
                                errorSets[currentSetIndex] = self.table[currentSetIndex][0]
                            errorSets[currentSetIndex] += str(self.numberedProductions.index(individualSet))
                            break
                #shift
                setShiftPosition = [-1] * len(self.allCharacters)
                for individualSet in self.allSets[currentSetIndex]:
                    individualSetArray = individualSet[1]
                    pointIndex = individualSetArray.index("~")
                    if pointIndex +1 !=  len(individualSetArray):
                        #we know we can shift
                        if  self.table[currentSetIndex][0] == None:
                            self.table[currentSetIndex][0] = "shift"
                            self.table[currentSetIndex][1] = setShiftPosition
                        if "reduce" in self.table[currentSetIndex][0]:
                            if currentSetIndex not in errorSets:
                                errorSets[currentSetIndex] = self.table[currentSetIndex][0]
                            errorSets[currentSetIndex] += " shift"
                            break
                        
                        characterShiftSet = self.getShift(currentSetIndex,individualSetArray[pointIndex+1],pointIndex)
                        if characterShiftSet == -2:
                            print("|BIG ERROR, -2-----------------")
                        setShiftPosition[self.allCharacters.index(individualSetArray[pointIndex+1])] = characterShiftSet

        #error
        if errorSets:
            print("we have errors with sets:" + str(errorSets.keys()))
            for i in errorSets.keys():
                print(errorSets[i])
                print(self.allSets[i])

    def printTable(self):
        for i in range(len(self.allSets)):
            print(str(self.allSets[i]) + ": "+ str(self.table[i]))

        

            


    

#print(["~","S"].index("~"))
# a = Parser("works.txt")

# symbols = []
# symbols += a.grammar.terminals
# symbols += a.grammar.nonterminals
# print(symbols)

# a.CanonicalCollection()
# a.createTable()
# a.printTable()
#print(a.table)
#a.prettyPrintSets()
#a.closure([["A",["~","A"]]])
#print(a.allSets)
#a.goto([["S",["~","S"]],["A",["C","~","A"]],["A",["C","~","S"]]],"S")

