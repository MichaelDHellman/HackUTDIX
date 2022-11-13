import csv
import scipy
from numpy import *
from enum import Enum

class Run:
    def __init__(self, start, end, section, len, name):
        self.name = name
        self.startpoint = start
        self.endpoint = end
        self.section = csvAsArr(section, len)
        self.duration = self.calcTime()
        self.cost = self.calcCost()
        self.efficiency = self.cost/(end-start)

    def calcTime(self):
        hoursElapsed = 0.0
        sum = 0.0
        for i in range(self.startpoint+1, self.endpoint):
            deltaD = self.section[i][0] - self.section[i-1][0]
            if (self.section[i][0] - self.section[i-1][0] > 0):
                hoursElapsed += (deltaD / float(self.section[i][1]))
            sum += self.section[i][1]
        #print("Average Speed: " + str(sum/float(self.section.size)))
        #print("Depth diff: " + str(endDep-startDep))
        return hoursElapsed
    
    def calcCost(self):
        if (self.name == "Buzz Drilldrin"):
            sum = 5000
            sum += (self.endpoint - self.startpoint) * 1.5
            return sum
        if (self.name == "AstroBit"):
            sum = 3000
            sum += (self.endpoint - self.startpoint)
            sum += 1500*self.duration
            return sum
        if (self.name == "Apollo"):
            sum = 1000
            sum += (self.endpoint - self.startpoint) * 4
            sum += 2500 * self.duration
            return sum
        if (self.name == "ChallengDriller"):
            return 10000
        

def calcRunCost(read):
    pass

def fillEmpties(csvRW):
    pass

def csvAsArr(inp, len):
    colArr = zeros((len-1, 5), dtype=float)
    for i, row in enumerate(inp):
        if (i == 0):
            continue
        for j, val in enumerate(row):
            if j < 5:
                colArr[i-1][j] = float(val)
    return colArr

#CALL SEEK(0) IF YOU WANT IT TO WORK
def calcRunTime(read,startpoint,endpoint):
    #Enumerate from startpoint
    hoursElapsed = 0.0
    prevDep = read[startpoint][0]
    startDep = read[startpoint][0]
    endDep = 0.0
    sum = 0.0
    #time from r1 to r2 = (r2.depth - r1.depth) / r2.rate
    for i in range(startpoint, endpoint-1):
        if (prevDep == float(read[i][0]) or read[i][0] <= 0 or read[i][1] <= 0):
            continue
        deltaD = 0.0
        if (read[i][0] != 0 and prevDep != 0):
            deltaD = float(read[i][0]) - prevDep
        if (float(read[i][1]) != 0):
            hoursElapsed += (deltaD / float(read[i][1]))
        if (read[i][0] != 0):
            prevDep = read[i][0]
        sum += read[i][1]
        endDep = read[i][0]
    return hoursElapsed
        
def getRunsList(read, finp):
    runs = []
    ends = getEndsList(read)
    start = 0
    finp.seek(0)
    len = sum(fromiter((1 for line in read), int))
    finp.seek(0)
    fArr = csvAsArr(read, len)
    finp.seek(0)
    names = getNamesList(read)
    for i,end in enumerate(ends):
        runs.append(Run(start,end,fArr, len, names[i]))
    return runs

def getNamesList(read):
    names = []
    prevID = -1
    prevName = ""
    next(read)
    start = next(read)
    prevID = start[5]
    prevName = start[6]
    names.append(start[6])
    final = 0
    for i,line in enumerate(read):
        if prevID != line[5]:
            names.append(line[6])
        elif prevName == "":
            prevName = line[6]
        elif prevName != line[6]:
            names.append(line[6])
        prevName = line[6]
        prevID = line[5]
        final = i
    return names

def getEndsList(read):
    endpoints = []
    prevID = -1
    prevName = ""
    next(read)
    start = next(read)
    prevID = start[5]
    prevName = start[6]
    final = 0
    for i,line in enumerate(read):
        if prevID != line[5]:
            endpoints.append(i+2)
        elif prevName == "":
            prevName = line[6]
        elif prevName != line[6]:
            endpoints.append(i+2)
        prevName = line[6]
        prevID = line[5]
        final = i
    endpoints.append(final)
    return endpoints

if __name__ == "__main__":
    csvfile = open("../data/Asteroid 1.csv", "r", newline='', encoding="utf-8-sig")
    csvReader = csv.reader(csvfile, delimiter=",")
    runsList = getRunsList(csvReader)
    length = sum(fromiter((1 for line in open("../data/Asteroid 1.csv")), int))
    runsList.append(length)
    colArr = zeros((length, 5), dtype=float)
    deltas = {0, 0, 0, 0, 0}
    csvfile.seek(0)
    next(csvReader)
    for i, row in enumerate(csvReader):
        for j, num in enumerate(row):
            if j > 4:
                break
            if num != '':
                colArr[i][j] = num
            else:
                colArr[i][j] = float(colArr[i-1][j]) + float(colArr[i+1][j]) / 2.0
        #print(colArr[i])
    start = 0
    for endP in runsList:
        csvfile.seek(0)
        print("Runtime: " + str(calcRunTime(colArr, start, endP)))
        start = endP
    csvfile.seek(0)
    next(csvfile)
    #for i in range(length):
    #    print(colArr[i])
    #print(colArr[0])
    #print(colArr[1])
    #print(scipy.stats.pearsonr(colArr[0], colArr[1]))