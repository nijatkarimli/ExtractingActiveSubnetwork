
import CreatingPopulationPhase
import CrossoverAndMutationPhase
import datetime
import math
import os

def isConnected(graph,verticesEncountered=None,startVertex=None,gDict=None):
    if verticesEncountered is None:
        verticesEncountered = set()
    if gDict is None:
        gDict={}
        for i in range(len(graph)):
            if graph[i]=="1":
                if len(CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"])>0:
                    gDict[CreatingPopulationPhase.ppiNodeList[i]] = []#
                    for j in range(len(CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"])):  #
                        if graph[
                            CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"][j]][
                                "index"]] == "1":  #
                            gDict[CreatingPopulationPhase.ppiNodeList[i]].append(
                                CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"][j])  ##
    vertices = list(gDict.keys())
    if not startVertex:
        startVertex = vertices[0]
    verticesEncountered.add(startVertex)
    if len(verticesEncountered) != len(vertices):
        for vertex in gDict[startVertex]:
            if vertex not in verticesEncountered:
                if isConnected(graph,verticesEncountered, vertex, gDict):
                    return True
    else:
        return True
    return False

def convertSubGraphToDictionary(wholeSubGraph):
    gDict = {}
    for i in range(len(wholeSubGraph)):
        if wholeSubGraph[i] == "1":
            gDict[CreatingPopulationPhase.ppiNodeList[i]] = []
            for j in range(len(CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"])):
                if wholeSubGraph[
                    CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"][j]][
                        "index"]] == "1":
                    gDict[CreatingPopulationPhase.ppiNodeList[i]].append(
                        CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"][j])
    return gDict

def findingPotentialNodes(subnetworkList, resultPopulationDict, newAverage):
    potentialNodes=[]
    for i in range(len(subnetworkList)):
        for j in range(len(CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"])):
            if (CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j]]["zValue"]) > newAverage and (CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j] not in resultPopulationDict[subnetworkList[i]]) and (CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j] not in [row[0] for row in potentialNodes]):
                potentialNodes.append([CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j],CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j]]["zValue"]])
    return potentialNodes


path = os.getcwd()+"allData\\FinalResultSubnetwork_" + str(CreatingPopulationPhase.input).split("\\")[1]
if os.path.exists(path):
    os.remove(path)
totalSum = 0
filenameRead = "allData\\resultSubnetwork_" + str(CreatingPopulationPhase.input).split("\\")[1]
f = open(filenameRead, "r")
context = f.readlines()
for i in range(len(context)):
    context[i] = context[i].rstrip()
    if i != 0 and i != len(context) - 1:
        totalSum += CreatingPopulationPhase.adjacencyDict[context[i]]["zValue"]


average = totalSum / (len(context) - 2)
z = totalSum / math.sqrt(len(context)-2)
resultZValue = context[0]
totalNode = len(context)-2
resultPopulation = context[len(context)-1]
context.pop(0)
context.pop(len(context)-1)
print(isConnected(resultPopulation))
resList = list(resultPopulation)
contextCopy = context.copy()


for i in range(len(contextCopy)):
    if CreatingPopulationPhase.adjacencyDict[contextCopy[i]]["zValue"] < average:
        resList[CreatingPopulationPhase.adjacencyDict[contextCopy[i]]["index"]] = "0"
        resultPopulation = "".join(resList)
        if isConnected(resultPopulation):
            context.pop(context.index(contextCopy[i]))
            totalNode -= 1
            totalSum -= CreatingPopulationPhase.adjacencyDict[contextCopy[i]]["zValue"]
        else:
            resList[CreatingPopulationPhase.adjacencyDict[contextCopy[i]]["index"]] = "1"
            resultPopulation = "".join(resList)

resultPopulation = "".join(resList)

newAverage = totalSum / totalNode
resultPopulationDict = convertSubGraphToDictionary(resultPopulation)
potensialNodes=findingPotentialNodes(context, resultPopulationDict, newAverage)

for i in range(len(potensialNodes)):
    context.append(potensialNodes[i][0])
    resList[CreatingPopulationPhase.adjacencyDict[potensialNodes[i][0]]["index"]] = "1"
    totalNode += 1
    totalSum += potensialNodes[i][1]

resultPopulation = "".join(resList)
for i in range(len(resList)):
    resList[i] = int(resList[i])
f = open("allData\\FinalResultSubnetwork_" + str(CreatingPopulationPhase.input).split("\\")[1], "w")
f.write(str(round(totalSum / math.sqrt(totalNode),3)))
f.write('\n')
for i in range(len(context)):
    subnetwork = ""
    subnetwork += "".join(context[i])
    f.write(subnetwork)
    f.write("\n")

f.write(str(isConnected(resultPopulation)))
f.write('\n')
f.write(resultPopulation)
f.close()

endTime = datetime.datetime.now()
CreatingPopulationPhase.getFileTime("Code ends: ", endTime)