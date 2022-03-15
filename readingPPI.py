import json


def readingPPINetwork():
    try:
        file = open("allData\\PPI.sif", "r")
    except FileNotFoundError:
        print("File not found")
    else:
        ppiEdgeList = []
        ppiNodeList = []
        context = file.readlines()  # reading all file at once
        for lines in context:  # lines is one line in all context
            nodePair1 = lines.split(" pp ")[0].rstrip()
            nodePair2 = lines.split(" pp ")[1].rstrip()
            if nodePair1 != nodePair2:  # remove unnecessary edges if they are not related to certain disease
                ppiEdgeList.append((nodePair1, nodePair2))
            if nodePair1 not in ppiNodeList:
                ppiNodeList.append(nodePair1)
            if nodePair2 not in ppiNodeList:
                ppiNodeList.append(nodePair2)
        file.close()

        adjacencyDict = {}
        indexValue = 0
        for i in range(len(ppiNodeList)):
            adjacencyDict[ppiNodeList[i]] = {}
            adjacencyDict[ppiNodeList[i]]["neigbors"] = []
            adjacencyDict[ppiNodeList[i]]["index"] = indexValue
            for j in range(len(ppiEdgeList)):
                if ppiNodeList[i] == ppiEdgeList[j][0] and ppiNodeList[i] != ppiEdgeList[j][1] and ppiEdgeList[j][1] not in adjacencyDict[ppiNodeList[i]]["neigbors"]:
                    adjacencyDict[ppiNodeList[i]]["neigbors"].append(ppiEdgeList[j][1])
                elif ppiNodeList[i] == ppiEdgeList[j][1] and ppiNodeList[i] != ppiEdgeList[j][0] and ppiEdgeList[j][0] not in adjacencyDict[ppiNodeList[i]]["neigbors"]:
                     adjacencyDict[ppiNodeList[i]]["neigbors"].append(ppiEdgeList[j][0])
            indexValue += 1
        #storing adjacency dictionary and PPI Node List to the file
        jsonAdjacencyStr = json.dumps(adjacencyDict)
        f=open("allData\\adjacency.json", "w")
        f.write(jsonAdjacencyStr)
        f.close()

        f=open("allData\\ppiNodeList.txt","w")
        for i in range(len(ppiNodeList)):
            f.write(str(ppiNodeList[i]))
            f.write("\n")
        f.close()

readingPPINetwork()