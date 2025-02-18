#!/usr/bin/python



import os

import sys

import codecs

import re

import locale

# sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 



featPrintPriority = ['af', 'name']



class Node() :

    def __init__(self,text,dummy=False) :

        self.text = text

        self.lex = None

        self.type = None

        self.__attributes = {}

        self.errors = []

        self.name = None

        self.parent = None

        self.parentRelation = None

        self.alignedTo = None

        self.fsList = None

        self.dummy = dummy



        if self.dummy == False :

            self.analyzeNode(self.text)



    def analyzeNode(self, text) :

        [token, tokenType, fsDict, fsList] = getTokenFeats(text.strip().split())

        attributeUpdateStatus = self.updateAttributes(token, tokenType, fsDict, fsList)

        if attributeUpdateStatus == 0 :

            self.errors.append("Can't update attributes for node")

            self.probSent = True



    

    def updateAttributes(self,token, tokenType, fsDict, fsList) :

        self.fsList = fsList

        self.lex = token

        self.type = tokenType

        for attribute in fsDict.keys() :

            self.__attributes[attribute] = fsDict[attribute]

        self.assignName()



    def assignName(self) :

        if 'name' in self.__attributes : 

            self.name = self.getAttribute('name')

        else :

            self.errors.append('No name for this token Node')

            

    def printValue(self) :

        return self.lex



    def printSSFValue(self, prefix, allFeat) :

        returnValue = [prefix , self.printValue() , self.type]

        if allFeat == False : 

            fs = ['<fs']

            for key in self.__attributes.keys() :

                fs.append(key + "='" + self.getAttribute(key) + "'")

            delim = ' '

            fs[-1] = fs[-1] + '>'

            

        else :

            fs = self.fsList

            delim = '|'

        return ['\t'.join(x for x in returnValue) + '\t' + delim.join(x for x in fs)]



    def getAttribute(self,key) :

        if key in self.__attributes :

            return self.__attributes[key]

        else :

            return None



    def addAttribute(self,key,value) :

        self.__attributes[key] = value



    def deleteAttribute(self,key) :

        del self.__attributes[key]

            

class ChunkNode() :

    

    def __init__(self, header) :

        self.text = []

        self.header = header

        self.footer = None

        self.nodeList = []

        self.parent = '0'

        self.parentPB = '0'

        self.__attributes = {}

        self.parentRelation = 'root'

        self.parentPBRelation = 'root'

        self.name = None

        self.type = None

        self.head = None

        self.isParent = False

        self.errors = []

        self.upper = None

        self.updateDrel()

        self.updatePBrel()

        self.type = None

        self.fsList = None



    def analyzeChunk(self)  :

        [chunkType,chunkFeatDict,chunkFSList] = getChunkFeats(self.header)

        self.fsList = chunkFSList

        self.type = chunkType

        self.updateAttributes(chunkFeatDict)

        self.text = '\n'.join([line for line in self.text])

    

    def updateAttributes(self,fsDict) :

        for attribute in fsDict.keys() :

            self.__attributes[attribute] = fsDict[attribute]

        self.assignName()

        self.updateDrel()

        self.updatePBrel()



    def assignName(self) :

        if 'name' in self.__attributes : 

            self.name = self.getAttribute('name')

        else :

            self.errors.append('No name for this chunk Node')

        

    def updateDrel(self) :

        if 'drel' in self.__attributes :

            drelList = self.getAttribute('drel').split(':')

            if len(drelList) == 2 :

                self.parent = drelList[1]

                self.parentRelation = self.getAttribute('drel').split(':')[0]

        elif 'dmrel' in self.__attributes :

            drelList = self.getAttribute('dmrel').split(':')

            if len(drelList) == 2 :

                self.parent = drelList[1]

                self.parentRelation = self.getAttribute('dmrel').split(':')[0]



    def updatePBrel(self) :

        if 'pbrel' in self.__attributes :

            pbrelList = self.getAttribute('pbrel').split(':')

            if len(pbrelList) == 2 :

                self.parentPB = pbrelList[1]

                self.parentPBRelation = self.getAttribute('pbrel').split(':')[0]



    def printValue(self) :

        returnString = []

        for node in self.nodeList :

            returnString.append(node.printValue())

        return ' '.join(x for x in returnString)



    def printSSFValue(self, prefix, allFeat) :

        returnStringList = []

        returnValue = [prefix , '((' , self.type]

        if allFeat == False : 

            fs = ['<fs']

            for key in self.__attributes.keys() :

                fs.append(key + "='" + self.getAttribute(key) + "'")

            delim = ' '

            fs[-1] = fs[-1] + '>'

            

        else :

            fs = self.fsList

            delim = '|'

        

        returnStringList.append('\t'.join(x for x in returnValue) + '\t' + delim.join(x for x in fs))

        nodePosn = 0

        for node in self.nodeList :

            nodePosn += 1

            if isinstance(node,ChunkNode) :

                returnStringList.extend(node.printSSFValue(prefix + '.' + str(nodePosn), allFeat))

            else :

                returnStringList.extend(node.printSSFValue(prefix + '.' + str(nodePosn), allFeat))

        returnStringList.append('\t' + '))')

        return returnStringList



    def getAttribute(self,key) :

        if key in self.__attributes :

            return self.__attributes[key]

        else :

            return None



    def addAttribute(self,key,value) :

        self.__attributes[key] = value



    def deleteAttribute(self,key) :

        del self.__attributes[key]



class Sentence() :

    def __init__(self, sentence, ignoreErrors = True, nesting = True, dummySentence = False) :

        self.ignoreErrors = ignoreErrors

        self.nesting = nesting

        self.sentence = None

        self.sentenceID = None

        self.sentenceType = None

        self.length = 0

        self.tree = None

        self.nodeList = []

        self.edges = {}

        self.edgesPB = {}

        self.nodes = {}

        self.tokenNodes = {}

        self.rootNode = None

        self.fileName = None

        self.comment = None

        self.probSent = False

        self.errors = []

        self.dummySentence = dummySentence

        if self.dummySentence == False :

            

            self.header = sentence.group('header')

            self.footer = sentence.group('footer')

            self.name = sentence.group('sentenceID')

            self.text = sentence.group('text')

            self.analyzeSentence()

        

    def analyzeSentence(self, ignoreErrors = False, nesting = True) :

        

        lastContext = self

        

        for line in self.text.split('\n') :

            stripLine = line.strip()

            

            if stripLine=="" :

                continue

            elif stripLine[0]=="<" and ignoreErrors == False :            

                    self.errors.append('Encountered a line starting with "<"')

                    self.probSent = True

            else :

                splitLine = stripLine.split()

                if len(splitLine)>0 and splitLine[0] == '))' :

                    

                    currentChunkNode.footer = line + '\n'

                    currentChunkNode.analyzeChunk()

                    lastContext = currentChunkNode.upper

                    currentChunkNode = lastContext



                elif len(splitLine)>1 and splitLine[1] == '((' :

                    currentChunkNode = ChunkNode(line + '\n')

                    currentChunkNode.upper = lastContext

                    currentChunkNode.upper.nodeList.append(currentChunkNode)

                    if currentChunkNode.upper.__class__.__name__ != 'Sentence' :

                        currentChunkNode.upper.text.append(line)

                    lastContext = currentChunkNode

                else :

                    currentNode = Node(line + '\n')

                    lastContext.nodeList.append(currentNode)

                    currentNode.upper = lastContext

                        

        # updateAttributesStatus = self.updateAttributes()

        # if updateAttributesStatus == 0 :

        #     self.probsent = True

        #     self.errors.append("Cannot update the Attributes for this sentence")

        

    def addEdge(self, parent , child) :

        if parent in self.edges.iterkeys() :

            if child not in self.edges[parent] : 

                self.edges[parent].append(child)

        else :

            self.edges[parent] = [child]



    def addEdgePB(self, parent , child) :

        if parent in self.edgesPB.iterkeys() :

            if child not in self.edgesPB[parent] : 

                self.edgesPB[parent].append(child)

        else :

            self.edgesPB[parent] = [child]



    def updateAttributes(self) :

        populateNodesStatus = self.populateNodes()

        populateEdgesStatus = self.populateEdges()

        populateEdgesPBStatus = self.populateEdgesPB()

        self.sentence = self.generateSentence()

        if populateEdgesStatus == 0 or populateNodesStatus == 0 or populateEdgesPBStatus == 0 :

            return 0

        return 1



    def printSSFValue(self, allFeat) :

        returnStringList = []

        returnStringList.append("<Sentence id='" + str(self.name) + "'>")

        if self.nodeList != [] :

            nodeList = self.nodeList

            nodePosn = 0

            for node in nodeList :

                nodePosn += 1

                returnStringList.extend(node.printSSFValue(str(nodePosn), allFeat))

        returnStringList.append( '</Sentence>\n')

        return '\n'.join(x for x in returnStringList)

        

    def populateNodes(self , naming = 'strict') :

        if naming == 'strict' : 

            for nodeElement in self.nodeList :

                assert nodeElement.name is not None

                self.nodes[nodeElement.name] = nodeElement

        return 1

    

    def populateEdges(self) :

        for node in self.nodeList :

            nodeName = node.name

            if node.parent == '0'  or node == self.rootNode:

                self.rootNode = node

                continue

            elif node.parent not in self.nodes.iterkeys() :

                return 0

            assert node.parent in self.nodes.iterkeys()

            self.addEdge(node.parent , node.name)

        return 1



    def populateEdgesPB(self) :

        for node in self.nodeList :

            nodeName = node.name

            if node.parentPB != '0' and node.parentPB not in self.nodes.iterkeys() :

                return 0

            if node.parentPB != '0' : 

                assert node.parentPB in self.nodes.iterkeys()

                self.addEdgePB(node.parentPB , node.name)

        return 1



    def generateSentence(self) :

        sentence = []

        for nodeName in self.nodeList :

            sentence.append(nodeName.printValue())

        return ' '.join(x for x in sentence)



class Document() :



    def __init__(self, fileName) :

        self.header = None

        self.footer = None

        self.text = None

        self.nodeList = []

        self.fileName = fileName

        self.upper = None

        self.header = None

        self.analyzeDocument()



    def analyzeDocument(self) :

        

        inputFD = codecs.open(self.fileName, 'r', encoding='utf8')

        self.text = inputFD.read()    

        self.header = re.findall(r'<head>.*?</head>', self.text, re.DOTALL)

        sentenceList = getSentenceIter(inputFD, self.text)

        for sentence in sentenceList :

            tree = Sentence(sentence, ignoreErrors = True, nesting = True)

            tree.upper = self

            self.nodeList.append(tree)

        inputFD.close()



def getAddressNode(address, node, level = 'ChunkNode') :

    

    ''' Returns the node referenced in the address string relative to the node in the second argument.

        There are levels for setting the starting address-base. These are "ChunkNode", "Node" , "Sentence" , "Document" , "Relative".

        The hierarchy of levels for interpretation is :

        "Document" -> "Sentence" -> "ChunkNode" -> "Node"

        "Relative" value starts the base address from the node which contains the address. This is also the default option.

    '''



    currentContext = node



    if level != 'Relative' : 

        while(currentContext.__class__.__name__ != level) :

            currentContext = currentContext.upper

            

    currentContext = currentContext.upper

    

    stepList = address.split('%')

    

    for step in stepList :

        if step == '..' :

            currentContext = currentContext.upper

        else :

            refNode = [iterNode for iterNode in currentContext.nodeList if iterNode.name == step][0]

            currentContext = refNode

    return refNode



def getChunkFeats(line) :

    lineList = line.strip().split()

    chunkType = None

    fsList = []

    if len(lineList) >= 3 : 

        chunkType = lineList[2]

        

    returnFeats = {}

    multipleFeatRE = r'<fs.*?>'

    featRE = r'(?:\W*)(\S+)=([\'|\"])?([^ \t\n\r\f\v\'\"]*)[\'|\"]?(?:.*)'

    fsList = re.findall(multipleFeatRE, ' '.join(lineList))

    for x in lineList :

        feat = re.findall(featRE, x)

        if feat!=[] :

            if len(feat) > 1 :

                returnErrors.append('Feature with more than one value')

                continue

            returnFeats[feat[0][0]] = feat[0][2]



    return [chunkType,returnFeats,fsList]



def getTokenFeats(lineList) :

    tokenType, token = None , None

    returnFeats = {}

    fsList = []

    if len(lineList) >=3 :

        tokenType = lineList[2]



    token = lineList[1]

    multipleFeatRE = r'<fs.*?>'

    featRE = r'(?:\W*)(\S+)=([\'|\"])?([^ \t\n\r\f\v\'\"]*)[\'|\"]?(?:.*)'

    fsList = re.findall(multipleFeatRE, ' '.join(lineList))

    for x in lineList :

        feat = re.findall(featRE, x)

        if feat!=[] :

            if len(feat) > 1 :

                returnErrors.append('Feature with more than one value')

                continue

            returnFeats[feat[0][0]] = feat[0][2]



    return [token,tokenType,returnFeats,fsList]

        

def getSentenceIter(inpFD, text) :



    sentenceRE = r'''(?P<complete>(?P<header><Sentence id=[\'\"]?(?P<sentenceID>.*?)[\'\"]?>)(?P<text>.*?)(?P<footer></Sentence>))'''

    return re.finditer(sentenceRE, text, re.DOTALL)



def folderWalk(folderPath):

    import os

    fileList = []

    for dirPath , dirNames , fileNames in os.walk(folderPath) :

        for fileName in fileNames : 

            fileList.append(os.path.join(dirPath , fileName))

    return fileList



if __name__ == '__main__' :

    

    inputPath = sys.argv[1]

    fileList = folderWalk(inputPath)

    newFileList = []

    for fileName in fileList :

        xFileName = fileName.split('/')[-1]

        if xFileName == 'err.txt' or xFileName.split('.')[-1] in ['comments','bak'] or xFileName[:4] == 'task' :

            continue

        else :

            newFileList.append(fileName)



    for fileName in newFileList :

        d = Document(fileName)

        for tree in d.nodeList : 
            print(tree.__dict__)

            for chunkNode in tree.nodeList :

                for node in chunkNode.nodeList :

                    print(node.__dict__)
