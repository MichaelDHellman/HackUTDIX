import csv
import CSVSanitize
import CSVUtils as utils
from numpy import *
import os

if __name__ == "__main__":
    for fname in os.listdir("../data"):
        fpath = os.path.join("../data/", fname)
        if (os.path.isfile(fpath) and ("sanitized_" not in fpath)):
            CSVSanitize.makeSanitized(fpath)
    filesList = []
    for fname in os.listdir("../data"):
        fpath = os.path.join("../data/", fname)
        if (os.path.isfile(fpath) and ("sanitized_" in fpath)):
            filesList.append(fpath)
    effAvgs = [0.0,0.0,0.0,0.0]
    counts = [0,0,0,0]
    for file in filesList:
        inp = open(file, "r", newline='', encoding="utf-8-sig")
        csvinp = csv.reader(inp, delimiter=',')
        inp.seek(0)
        print(file)
        runs = utils.getRunsList(csvinp, inp)
        for run in runs:
            print("Run of " + run.name + " Duration: " + str(run.duration) + " Cost: " + str(run.cost) + " Efficiency: " + str(run.efficiency))
        
        for run in runs:
            if (run.name == "Buzz Drilldrin"):
                effAvgs[0] += run.efficiency
                counts[0] += 1
            if (run.name == "AstroBit"):
                effAvgs[1] += run.efficiency
                counts[1] += 1
            if (run.name == "Apollo"):
                effAvgs[2] += run.efficiency
                counts[2] += 1
            if (run.name == "ChallengDriller"):
                effAvgs[3] += run.efficiency
                counts[3] += 1
    for i in range(4):
        if counts[i] > 0:
            effAvgs[i] = effAvgs[i]/counts[i]
    bitsArr = ["Buzz Drilldrin", "AstroBit", "Apollo","ChallengDriller"]
    print('\n')
    for i,n in enumerate(bitsArr):
        print("Average efficiency of " + n + " is: " + str(effAvgs[i]))
            
            
