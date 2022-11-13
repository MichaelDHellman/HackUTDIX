import csv
import scipy
from numpy import *
from enum import Enum
import os

ROLLING_SIZE = 5

def makeSanitized(filename):
    finp = open(filename, 'r',newline='', encoding="utf-8-sig")
    fout = open("../data/sanitized_" + filename[filename.rfind('/')+1:], "w", newline='')
    csvinp = csv.reader(finp)
    csvout = csv.writer(fout)
    length = sum(fromiter((1 for line in finp), int))
    finp.seek(0)
    colArr = zeros((length-1, 5), dtype=float)
    movings = zeros((5, length-1), dtype=float)
    ids = [None] * (length-1)
    names = [None] * (length - 1)
    next(csvinp)
    #colArr construct
    for i, row in enumerate(csvinp):
        for j, val in enumerate(row):
            if j > 4:
                if j == 5:
                    ids[i] = val
                if j == 6:
                    names[i] = val
                continue
            if val == '':
                #No valid instances of 0.0 exist, so safe
                colArr[i][j] = 0.0
            else:
                colArr[i][j] = val
    for i in range(5):
        movings[i] = convolve(colArr[ :,i], ones(ROLLING_SIZE), 'same') / (ROLLING_SIZE-1)
    #remove errors pass
    for i, row in enumerate(colArr):
        for j, val in enumerate(row):
            if (val <= 0.0):
                if movings[j][i] > 0.0:
                    colArr[i][j] = movings[j][i]
                else:
                    colArr[i][j] = 1.0
            elif (movings[j][i] == 0.0 or abs(val)/abs(movings[j][i]) > 20 or abs(val)/abs(movings[j][i]) < 0.1):
                if (movings[j][i] != 0.0):
                    colArr[i][j] = round(movings[j][i], 3)
                else:
                    colArr[i][j] = 1.0
    csvout.writerow("BIT_DEPTH,RATE_OF_PENETRATION,HOOK_LOAD,DIFFERENTIAL_PRESSURE,WEIGHT_ON_BIT,DRILL_BIT_ID,DRILL_BIT_NAME".split(','))
    for i in range(length-1):
        csvout.writerow([round(colArr[i][0], 2),round(colArr[i][1], 2),round(colArr[i][2], 2),round(colArr[i][3], 2),round(colArr[i][4], 2), ids[i], names[i]])




if __name__ == "__main__":
    flist = ""
    for fname in os.listdir("../data"):
        fpath = os.path.join("../data/", fname)
        if (os.path.isfile(fpath) and ("sanitized_" not in fpath)):
            makeSanitized(fpath)
    makeSanitized("../data/Asteroid 1.csv")