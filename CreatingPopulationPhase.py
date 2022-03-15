import math
import random
import statistics
import json
import os
import datetime

# reading disease node and store
def readingDiseaseNode(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("File not found")
    else:
        diseaseNodeDict = {}  # dictionary to store nodes and their scores
        context = file.readlines()  # reading all file at once
        for lines in context:  # lines is one line in all context
            # storing nodes and their values in dictionary line by line
            diseaseNodeDict[lines.split("\t")[0]] = float(lines.split("\t")[1])
        file.close()
        return diseaseNodeDict


# reading the whole PPI network, eliminate unnecessary edges and store it
def gettingPPI(diseaseNodeDict):
    diseaseNodeList = list(diseaseNodeDict.items())  # because of getting index of node, i copy my dictionary to list
    diseaseNodeListName = list(diseaseNodeDict.keys())
    try:
        f = open("allData\\adjacency.json", "r")
    except FileNotFoundError:
        print("File not found")
    else:
        adjacencyStr = f.readline()
        f.close()
        adjacencyDict = json.loads(adjacencyStr)
        try:
            f = open("allData\\ppiNodeList.txt", "r")
        except FileNotFoundError:
            print("File not found")
        else:
            ppiNodeList = f.readlines()
            f.close()
            tempValue = []
            for i in range(len(ppiNodeList)):
                ppiNodeList[i] = ppiNodeList[i].rstrip()
                if ppiNodeList[i] in diseaseNodeListName:
                    tempIndex = diseaseNodeListName.index(ppiNodeList[i])
                    adjacencyDict[ppiNodeList[i]]["pValue"] = diseaseNodeList[tempIndex][1]
                    tempValue.append((1-adjacencyDict[ppiNodeList[i]]["pValue"]))
                else:
                    adjacencyDict[ppiNodeList[i]]["pValue"] = 0.9999999999999 #0.999999
                    tempValue.append((1-adjacencyDict[ppiNodeList[i]]["pValue"]))

            zValue = calculateZvalue(tempValue)
            for i in range(len(ppiNodeList)):
                adjacencyDict[ppiNodeList[i]]["zValue"] = zValue[i]
            diseaseNodeList = list(diseaseNodeDict.items())
            diseaseNodeListName = list(diseaseNodeDict.keys())
            sortedNodeDict = {k: v for k, v in sorted(diseaseNodeDict.items(), key=lambda item: item[1], reverse=False)}
            sortedNodeList = list(sortedNodeDict.items())
            return diseaseNodeList, sortedNodeList, adjacencyDict, diseaseNodeListName, ppiNodeList


def calculateZvalue(oneMinuspValue):
    zValue = []
    standartDeviation = 1
    arithMean = 0
    for i in range(len(oneMinuspValue)):
        zValue.append(statistics.NormalDist(mu=arithMean, sigma=standartDeviation).inv_cdf(oneMinuspValue[i]))
    return zValue


# creating initial population
def creatingInitialPopulation(diseaseNodeList, sortedNodeList, adjacencyDict, ppiNodeList):
    numberOfMaxNeigbors = 100
    lineOfInitialPopulation = 100
    vec = "x" * lineOfInitialPopulation
    initialPopulation = list(vec)
    count = 0
    initialPopulationIndex = 0
    numberOfNodeInitialPopulation = 0
    while initialPopulationIndex < lineOfInitialPopulation:
        queue = []
        v = "0" * len(ppiNodeList)
        vecRep = list(v)
        if initialPopulationIndex <= lineOfInitialPopulation * 0.8:
            firstSorted = sortedNodeList[count][0]
            firstSortedIndex = adjacencyDict[firstSorted]["index"]
            vecRep[firstSortedIndex] = "1"
        else:
            firstSortedIndex = random.randint(0, len(ppiNodeList) - 1)
            firstSorted = ppiNodeList[firstSortedIndex]
            vecRep[firstSortedIndex] = "1"
        visited = [False] * len(adjacencyDict)
        queue.append(firstSorted)
        while queue:
            last = queue[random.choice([i for i in range(0, len(queue))])]
            keyIndex = adjacencyDict[last]["index"]
            vecRep[keyIndex] = "1"
            numberOfNodeInitialPopulation += 1
            if numberOfNodeInitialPopulation >= numberOfMaxNeigbors:
                break
            for i in range(len(adjacencyDict[last]["neigbors"])):
                if visited[adjacencyDict[adjacencyDict[last]["neigbors"][i]]["index"]] == False and numberOfNodeInitialPopulation < numberOfMaxNeigbors:
                    queue.append(adjacencyDict[last]["neigbors"][i])
                if numberOfNodeInitialPopulation >= numberOfMaxNeigbors:
                    break
            visited[adjacencyDict[last]["index"]] = True
            queue.pop(queue.index(last))
        sum = 0
        for i in range(len(vecRep)):
            if vecRep[i] == "1":
                sum += 1
        if sum > 1:
            if vecRep not in initialPopulation:
                initialPopulation[initialPopulationIndex] = vecRep
                initialPopulationIndex += 1
            count += 1
            numberOfNodeInitialPopulation = 0
        else:
            count += 1
            numberOfNodeInitialPopulation = 0
    f = open("allData\\initialPopulation.txt", "a")
    for i in range(len(initialPopulation)):
        for j in range(len(initialPopulation[0])):
            v = "".join(str(initialPopulation[i][j]))
            f.write(v)
        f.write("\n")
    f.close()
    return initialPopulation


def calculateFitnessValueInitial(adjacencyDict, initialPopulation, ppiNodeList):
    fitnessValue = []
    currentFitnessValue = 0
    node = 0
    for i in range(len(initialPopulation)):
        for j in range(len(initialPopulation[0])):
            if initialPopulation[i][j] == "1":
                node += 1
                currentFitnessValue += adjacencyDict[ppiNodeList[j]]["zValue"]
        fitnessValue.append(round(currentFitnessValue / math.sqrt(node), 3))
        currentFitnessValue = 0
        node = 0
    maxValueFitness = max(fitnessValue)
    maxValueFitnessIndex = fitnessValue.index(maxValueFitness)
    return fitnessValue, maxValueFitness, maxValueFitnessIndex


def calculateFitnessValue(adjacencyDict, ppiNodeList, initialPopulation):
    currentFitnessValue = 0
    node = 0
    for i in range(len(initialPopulation)):
        if initialPopulation[i] == "1":
            node += 1
            currentFitnessValue += adjacencyDict[ppiNodeList[i]]["zValue"]
    if node != 0:
        return round(currentFitnessValue / math.sqrt(node), 3)
    else:
        return 0


def getFileTime(sectionName, differenceTime):
    file_time = open("allData\\time.txt", "a")
    file_time.write(sectionName + str(differenceTime))
    file_time.write("\n")
    file_time.close()


# main
try:
    startTime = datetime.datetime.now()
    getFileTime("Code Starts: ", startTime)
    path = os.getcwd()+"allData\\initialPopulation.txt"
    if os.path.exists(path):
        os.remove(path)
    input = "allData\\data10.txt"
    diseaseNodeDict = readingDiseaseNode(input)
    diseaseNodeList, sortedNodeList, adjacencyDict, diseaseNodeListName, ppiNodeList = gettingPPI(diseaseNodeDict)
    initialPopulation = creatingInitialPopulation(diseaseNodeList, sortedNodeList, adjacencyDict, ppiNodeList)
    EndTime = datetime.datetime.now()
    differenceTime = EndTime - startTime
    getFileTime("After initial population created: ", differenceTime)
    startFitnessInitial = datetime.datetime.now()
    fitnessValue, maxInitialFitnessValue, maxInitialFitnessValueIndex = calculateFitnessValueInitial(adjacencyDict, initialPopulation, ppiNodeList)
    getFileTime("Maximum initial fitness value: ", maxInitialFitnessValue)
    getFileTime("Maximum initial fitness value index: ", maxInitialFitnessValueIndex)
    endFitnessInitial = datetime.datetime.now()
    totalFitnessInitial = endFitnessInitial - startFitnessInitial
    getFileTime("Time consumed for fitness initial calculations: ", totalFitnessInitial)
except:
    print("Something goes wrong")
