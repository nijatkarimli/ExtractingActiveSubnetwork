import random
import math
import CreatingPopulationPhase
import datetime

def readInitial():
    try:
        file = open("allData\\initialPopulation.txt", "r")
    except FileNotFoundError:
        print("File not found")
    else:
        initialPopulation = file.readlines()
        return initialPopulation


def crossover(initialPopulation, totalCrossoverTime, totalMutationTime, totalFitnessTime, crosIter, forRandomIter):
    startCrossoverTime = datetime.datetime.now()
    infeasiblePopulationToCrossover=[]
    status = isFeasibleToCrossover(initialPopulation, infeasiblePopulationToCrossover, crosIter, forRandomIter)
    if status[0]:
        indexParent1 = status[1]
        indexParent2 = status[2]
        isCommon = status[3]#child-lar and-lanmis
        wholeSubGraph = status[4]#childler or-lanmis
        wholeSubGraphDict = convertSubGraphToDictionary(wholeSubGraph)

        for i in range(len(isCommon)):
            if isCommon[i] == 1:
                if len(wholeSubGraphDict[CreatingPopulationPhase.ppiNodeList[i]]) >= 2:#bolunecek ortak node-nin en az 2 edgesi olması
                    childAfterCrossover1, childAfterCrossover2 = divideGraph(wholeSubGraph, i, wholeSubGraphDict)
                    endCrossoverTime = datetime.datetime.now()
                    totalCrossoverTime += (endCrossoverTime - startCrossoverTime)
                    startFitnessTime = datetime.datetime.now()
                    fitnessAfterCrossover1 = CreatingPopulationPhase.calculateFitnessValue(CreatingPopulationPhase.adjacencyDict, CreatingPopulationPhase.ppiNodeList, childAfterCrossover1)
                    fitnessAfterCrossover2 = CreatingPopulationPhase.calculateFitnessValue(CreatingPopulationPhase.adjacencyDict, CreatingPopulationPhase.ppiNodeList, childAfterCrossover2)
                    comparisonIndexParents = [indexParent1, indexParent2]
                    endFitnessTime = datetime.datetime.now()
                    totalFitnessTime += endFitnessTime - startFitnessTime

                    startMutationTime = datetime.datetime.now()
                    subnetworkList, child1TotalZ = getSubnetwork(childAfterCrossover1)
                    subnetworkList, fitnessAfterMutation1, childAfterMutation1 = enrichment(subnetworkList, childAfterCrossover1, child1TotalZ)
                    endMutationTime = datetime.datetime.now()
                    totalMutationTime += (endMutationTime - startMutationTime)
                    resultingValue1 = max(fitnessAfterMutation1, fitnessAfterCrossover1)
                    if resultingValue1 == fitnessAfterMutation1:
                        resultingChild1 = childAfterMutation1
                    else:
                        resultingChild1 = childAfterCrossover1
                    for j in range(len(comparisonIndexParents)):
                        startFitnessTime = datetime.datetime.now()
                        if resultingValue1 > CreatingPopulationPhase.fitnessValue[comparisonIndexParents[j]]:
                            initialPopulation[comparisonIndexParents[j]] = "".join(resultingChild1)
                            CreatingPopulationPhase.fitnessValue[comparisonIndexParents[j]] = resultingValue1
                            if comparisonIndexParents[j] in infeasiblePopulationToCrossover:
                                infeasiblePopulationToCrossover.pop(
                                    infeasiblePopulationToCrossover.index(comparisonIndexParents[j]))
                            comparisonIndexParents.pop(j)
                            endFitnessTime = datetime.datetime.now()
                            totalFitnessTime += endFitnessTime - startFitnessTime
                            break
                        endFitnessTime = datetime.datetime.now()
                        totalFitnessTime += endFitnessTime - startFitnessTime

                    startMutationTime = datetime.datetime.now()
                    subnetworkList, child1TotalZ = getSubnetwork(childAfterCrossover2)
                    subnetworkList, fitnessAfterMutation2, childAfterMutation2 = enrichment(subnetworkList, childAfterCrossover2, child1TotalZ)
                    endMutationTime = datetime.datetime.now()
                    totalMutationTime += (endMutationTime - startMutationTime)
                    resultingValue2 = max(fitnessAfterMutation2, fitnessAfterCrossover2)
                    if resultingValue2 == fitnessAfterMutation2:
                        resultingChild2 = childAfterMutation2
                    else:
                        resultingChild2 = childAfterCrossover2
                    for j in range(len(comparisonIndexParents)):
                        startFitnessTime = datetime.datetime.now()
                        if resultingValue2 > CreatingPopulationPhase.fitnessValue[comparisonIndexParents[j]]:
                            initialPopulation[comparisonIndexParents[j]] = "".join(resultingChild2)
                            CreatingPopulationPhase.fitnessValue[comparisonIndexParents[j]] = resultingValue2
                            if comparisonIndexParents[j] in infeasiblePopulationToCrossover:
                                infeasiblePopulationToCrossover.pop(
                                    infeasiblePopulationToCrossover.index(comparisonIndexParents[j]))
                            comparisonIndexParents.pop(j)
                            endFitnessTime = datetime.datetime.now()
                            totalFitnessTime += endFitnessTime - startFitnessTime
                            break
                        endFitnessTime = datetime.datetime.now()
                        totalFitnessTime += endFitnessTime - startFitnessTime
                    ####
                    break
    else:
        infeasiblePopulationToCrossover.append(status[1])
    return initialPopulation, totalCrossoverTime, totalMutationTime, totalFitnessTime

def divideGraph(wholeSubGraph,index,wholeSubGraphDict):
    neigbors= wholeSubGraphDict[CreatingPopulationPhase.ppiNodeList[index]]
    c1="0"*len(wholeSubGraph)
    c2="0"*len(wholeSubGraph)
    childList1=list(c1)
    childList2=list(c2)
    childList1[index]="1"
    childList2[index]="1"
    visited1=[CreatingPopulationPhase.ppiNodeList[index]]
    visited2=[CreatingPopulationPhase.ppiNodeList[index]]
    mode=0
    #initial division
    for i in range(len(neigbors)):
        if mode==0:
            childList1[CreatingPopulationPhase.adjacencyDict[neigbors[i]]["index"]]="1"
            visited1.append(neigbors[i])
            mode=1
        else:
            childList2[CreatingPopulationPhase.adjacencyDict[neigbors[i]]["index"]]="1"
            visited2.append(neigbors[i])
            mode=0
    #initial division end
    #further division
    for t in range(1,len(visited1)):
        queue = []
        visited = [False] * len(CreatingPopulationPhase.adjacencyDict)
        queue.append(visited1[t])
        while queue:
            last = queue[0]
            keyIndex = CreatingPopulationPhase.adjacencyDict[last]["index"]
            childList1[keyIndex] = "1"
            if last not in visited1:
                visited1.append(last)
            for i in range(len(CreatingPopulationPhase.adjacencyDict[last]["neigbors"])):
                if (CreatingPopulationPhase.adjacencyDict[last]["neigbors"][i] in wholeSubGraphDict[last]) and (visited[CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[last]["neigbors"][i]]["index"]] == False) and (CreatingPopulationPhase.adjacencyDict[last]["neigbors"][i] not in visited2):
                    queue.append(CreatingPopulationPhase.adjacencyDict[last]["neigbors"][i])
            visited[CreatingPopulationPhase.adjacencyDict[last]["index"]] = True
            queue.pop(0)

    for t in range(len(childList2)):
        if wholeSubGraph[t]==1 and childList1[t]=="0":
            childList2[t]="1"
    #further division end
    child1="".join(childList1)
    child2="".join(childList2)
    return child1,child2


def convertSubGraphToDictionary(wholeSubGraph):
    gDict = {}
    for i in range(len(wholeSubGraph)):
        if wholeSubGraph[i] == 1:
            gDict[CreatingPopulationPhase.ppiNodeList[i]] = []
            for j in range(len(CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"])):
                if wholeSubGraph[
                    CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"][j]][
                        "index"]] == 1:
                    gDict[CreatingPopulationPhase.ppiNodeList[i]].append(
                        CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["neigbors"][j])
    return gDict


def isFeasibleToCrossover(initialPopulation,infeasiblePopulationToCrossover, crosIter, forRandomIter, currentParent2=None):
    isCommon=[]
    wholeSubGraph=[]
    if crosIter <= 100:
        indexParent1 = crosIter-1
        indexParent2 = random.choice([i for i in range(0, len(initialPopulation)) if i not in infeasiblePopulationToCrossover])
    else:
        indexParent1 = random.choice([i for i in range(0, len(initialPopulation)) if i not in infeasiblePopulationToCrossover])
        if crosIter <= forRandomIter:
            indexParent2 = 0
        else:
            indexParent2 = random.choice([i for i in range(0, len(initialPopulation)) if i not in infeasiblePopulationToCrossover])
    currentParent1 = list(initialPopulation[indexParent1])
    for i in range(0, len(currentParent1)):
        currentParent1[i] = int(currentParent1[i])
    for i in range(indexParent2, len(initialPopulation)):
        if i != indexParent1:
            tempParent2 = list(initialPopulation[i])
            for j in range(0, len(tempParent2)):
                tempParent2[j] = int(tempParent2[j])
            for k in range(len(tempParent2)):
                isCommon.append(currentParent1[k] & tempParent2[k])
            if sum(isCommon) > 0:
                for k in range(len(tempParent2)):
                    wholeSubGraph.append(currentParent1[k] | tempParent2[k])
                currentParent2=tempParent2
                indexParent2=i
                break
            else:
                isCommon=[]
    if currentParent2==None:
        return [False, indexParent1]
    else:
        return [True, indexParent1, indexParent2, isCommon, wholeSubGraph]


def checkMaximumFitnessInitialPopulation():
    maxFitnessValue = max(CreatingPopulationPhase.fitnessValue)
    maxFitnessValueIndex = CreatingPopulationPhase.fitnessValue.index(max(CreatingPopulationPhase.fitnessValue))
    return maxFitnessValue, maxFitnessValueIndex


def activeSubnetwork(initialPopulation):
    subnetwork=[]
    maxValue, maxIndex = checkMaximumFitnessInitialPopulation()
    resultPopulation=initialPopulation[maxIndex]
    resultPopulation=resultPopulation.rstrip()
    for i in range(len(resultPopulation)):
        if resultPopulation[i] == "1":
            subnetwork.append(CreatingPopulationPhase.ppiNodeList[i])
    print(maxValue)
    storeResult(maxValue)
    return subnetwork, maxValue, resultPopulation


def storeResult(maxValue):
    file_time = open("allData\\output.txt", "a")
    file_time.write(str(maxValue))
    file_time.write("\n")
    file_time.close()

def getSubnetwork(child):
    subnetwork=[]
    childTotalZ=0
    for i in range(len(child)):
        if child[i]=="1":
            subnetwork.append(CreatingPopulationPhase.ppiNodeList[i])
            childTotalZ += CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.ppiNodeList[i]]["zValue"]
    return subnetwork, childTotalZ


def findingLeaf(subnetworkList,resultPopulation):
    resultPopulationList=list(resultPopulation)
    for i in range(len(resultPopulationList)):
        resultPopulationList[i]=float(resultPopulationList[i])
    resultPopulationDict=convertSubGraphToDictionary(resultPopulationList)
    visited=[]
    queue=[]
    leafNodes=[]
    queue.append(subnetworkList[0])
    while queue:
        last = queue[0]
        if last not in visited:
            visited.append(last)
        count = 0
        for j in range(len(resultPopulationDict[last])):
            if resultPopulationDict[last][j] not in visited:
                queue.append(resultPopulationDict[last][j])
            else:
                count += 1
        if count == len(resultPopulationDict[last]) and last not in [row[0] for row in leafNodes]:
           leafNodes.append([last, CreatingPopulationPhase.adjacencyDict[last]["zValue"]])
        queue.pop(0)
    return leafNodes, resultPopulationDict


def findingPotentialNodes(subnetworkList, resultPopulationDict, leafNodes):
    potentialNodes=[]
    for i in range(len(subnetworkList)):
        if subnetworkList[i] not in [row[0] for row in leafNodes]:
            for j in range(len(CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"])):
                if (CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j] not in resultPopulationDict[subnetworkList[i]]) and (CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j] not in [row[0] for row in potentialNodes]):
                    potentialNodes.append([CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j],CreatingPopulationPhase.adjacencyDict[CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["neigbors"][j]]["zValue"]])
    return potentialNodes


def addRemoveNode(subnetworkList,leafNodes,potentialNodes,childTotalZ):
    leafValue=[row[1] for row in leafNodes]
    potentialValue=[row[1] for row in potentialNodes]
    limit1 = 0
    limit2 = 0
    coin = random.random()
    if coin < 0.5:
        limitBorder1 = 500
        limitBorder2 = 500
    else:
        limitBorder1 = len(leafValue)
        limitBorder2 = len(potentialValue)

    average = childTotalZ/len(subnetworkList)
    for i in range(len(leafValue)):
        if leafNodes[i][1] < average and limit1 < limitBorder1:
            subIndex = subnetworkList.index(leafNodes[i][0])
            subnetworkList.pop(subIndex)
            limit1 += 1
        if limit1 >= limitBorder1:
            break
    limitCount("Number of removing (Leaf) node: ", limit1, limitBorder1)
    for i in range(len(potentialValue)):
        if average < potentialNodes[i][1] and limit2 < limitBorder2:
            subnetworkList.append(potentialNodes[i][0])
            limit2 += 1
        if limit2 >= limitBorder2:
            break
    limitCount("Number of adding (potential) node: ", limit2, limitBorder2)
    return subnetworkList


def limitCount(stringData, writingData, limitBorder):
    file_limit = open("allData\\limitCount.txt", "a")
    file_limit.write("Limit Border: " + str(limitBorder) + "\n")
    file_limit.write(stringData + str(writingData))
    file_limit.write("\n")
    file_limit.close()


def gettingNewValue(subnetworkList):
    resultScore=0
    node=0
    vec="0"*len(CreatingPopulationPhase.adjacencyDict)
    vecList=list(vec)
    for i in range(len(subnetworkList)):
        resultScore+=CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["zValue"]
        node+=1
        vecList[CreatingPopulationPhase.adjacencyDict[subnetworkList[i]]["index"]]="1"
    resultScore=round(resultScore/math.sqrt(node), 3)
    resultPopulation="".join(vecList)
    return resultScore, resultPopulation


def enrichment(subnetworkList,resultPopulation,childTotalZ):
    leafNodes, resultPopulationDict = findingLeaf(subnetworkList, resultPopulation)
    potentialNodes = findingPotentialNodes(subnetworkList, resultPopulationDict, leafNodes)
    subnetworkList = addRemoveNode(subnetworkList, leafNodes, potentialNodes, childTotalZ)
    resultScore, resultPopulation = gettingNewValue(subnetworkList)
    return subnetworkList, resultScore, resultPopulation


currentIter = 0
iterationLimit =100000
forRandomIter =1500
minBreakIter =2000
compareValue = [i for i in range(1, iterationLimit) if i % 100 == 0]
initialPopulation = readInitial()
for i in range(len(initialPopulation)):
    initialPopulation[i] = initialPopulation[i].rstrip()
oldMaxValue = 0
breakIter = 0
totalCrossoverTime = datetime.timedelta(0)
totalMutationTime = datetime.timedelta(0)
totalFitnessTime = datetime.timedelta(0)
while True:
    currentIter += 1
    initialPopulation, totalCrossoverTime, totalMutationTime, totalFitnessTime = crossover(initialPopulation, totalCrossoverTime, totalMutationTime, totalFitnessTime,currentIter,forRandomIter)
    if currentIter in compareValue:
        subnetworkList, maxValue, resultPopulation = activeSubnetwork(initialPopulation)
        if currentIter > minBreakIter:
            if maxValue == oldMaxValue:
                breakIter += 1
            else:
                oldMaxValue = maxValue
                breakIter = 0
    if breakIter == 9:
        print(currentIter)
        break
startFitnessTime = datetime.datetime.now()
subnetworkList, maxValue, resultPopulation = activeSubnetwork(initialPopulation)
endFitnessTime = datetime.datetime.now()
totalFitnessTime += endFitnessTime - startFitnessTime
CreatingPopulationPhase.getFileTime("total crossover time: ", totalCrossoverTime)
CreatingPopulationPhase.getFileTime("total mutation time: ", totalMutationTime)
CreatingPopulationPhase.getFileTime("total fitness time: ", totalFitnessTime)
f = open("allData\\resultSubnetwork_" + str(CreatingPopulationPhase.input).split("\\")[1], "w")
f.write(str(maxValue))
f.write('\n')
for i in range(len(subnetworkList)):
    subnetwork = ""
    subnetwork += "".join(subnetworkList[i])
    f.write(subnetwork)
    f.write("\n")
f.write(resultPopulation)
f.close()
