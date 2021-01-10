"""
    Combines all data from different files in given directory, and saves as "combinedData.txt" in same directory.
"""

import os
#data placed at "C:/Users/merli/Documents/Data_Mining/FilteredData"

def combineData(dataDir, outfilename = "combinedData.txt"):

    writeFileName = dataDir+outfilename
    wf = open (writeFileName, "w+")
    
    for readFile in os.listdir(dataDir):
        if (readFile != outfilename):
            thisFile = open(dataDir+readFile)
            thistxt = thisFile.read()
            wf.write(thistxt)
            thisFile.close()
    wf.close()

    

