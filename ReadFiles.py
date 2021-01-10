"""
Reads .run.json file in all subdirectories of given directory, filters according to specifications, and writes all cards of filtered decked to specified file.

Filtering:
    Class = Ironclad or Silent (to be specified)
    Floor reached > 49      (only 'finished' decks)
    Ascension = True
    Ascension level > 17    (only decks of 'experienced' players)

Decks can be written either as list of cards, or as vector using the defined dictionary.

"""

##  Imports, Constants, Names
#Class to be checked
#thisClass = 'Ironclad'
thisClass = 'Silent'

#imports
import os
os.chdir("C:/Users/merli/Documents/Data_Mining/")   #shouldn't be required, right?
import numpy as np
import json
import sys
sys.path.append("..")
import toolbox
import time         #for testing purposes

#names of paths
here = "C:/Users/merli/Documents/Data_Mining/"
dirName = here+"Data/"
if (thisClass=='Ironclad'):
    writeDir = here+"FilteredData/"
elif (thisClass == 'Silent'):
    writeDir = here+"FilteredDataSilent/"
    
#Json names + desired values
JSClassName = 'character_chosen'
if (thisClass == 'Ironclad'):
    JSClassVal = 'IRONCLAD'
elif (thisClass == 'Silent'):
    JSClassVal = 'THE_SILENT'

JSIsAssName = 'is_ascension_mode'
JSIsAssVal = True               #note: earlier then ascension_level, so interesting?

JSAssName = 'ascension_level'
JSAssValMin = 17                #note: last value, so might be easy to check?

JSFloorName = 'floor_reached'
JSFloorValMin = 49              #note: second element

JSDeckName = 'master_deck'

#import card dictionary
from toolbox.cardDicts import classCardDict
cardDict = classCardDict(thisClass)
nmbrCards = len(cardDict)

#error variables for checking validity result
nmbrKeyErrors = 0
errorCard = []
nmbrErrors = 0
nmbrOutlierErrors = 0

##  setting up for one month:

#for months in ["2019-06"]:            #alternative for manually doing just one month.
for months in os.listdir(dirName):
    thisMonthDirName = dirName+months
    thisWriteFile = writeDir+months+".txt"
    print ("doing month "+months)
    allDecks = []
    i=0

    start = time.time() #variables for testing purposes
    
##  filtering decks, saving them as array of names

    for days in os.listdir(thisMonthDirName):
        thisDay = thisMonthDirName+'/'+days
        for file in os.listdir(thisDay):
            thisFile = open(thisDay+"/"+file)
            try:
                thisJson = json.load(thisFile)                                                                              #create python dictionary with data
            except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
                nmbrErrors +=1
            try:
                if (thisJson[JSClassName] == JSClassVal and thisJson[JSAssName] >JSAssValMin and thisJson[JSFloorName] <49 ):        #filter correct runs
                    allDecks.append(thisJson[JSDeckName])                                                        #save deck to array
            except (KeyError, TypeError) as e:
                nmbrErrors +=1
    
    ##  write raw decklists to file (not used)
    """
    with open(thisWriteFile, "w") as outFile:
        for i in allDecks:
            outFile.write(",".join(i) + "\n")
    """
    
    ##  write decklists as vectors, using dictionary
    
    allVectors = []

    
    for i in range (len(allDecks)):
        try:
            thisDeck = allDecks[i]
            thisVector = np.zeros(nmbrCards)
            for j in range (len (thisDeck)):            #for every card, +1 to thisVector[i], with i from dict.
                thisCard = thisDeck[j]
                if (thisCard[len(thisCard) -2] == "+" or thisCard[len(thisCard)-1] == 'R'):
                    thisCard = thisCard[:-2]            #remove characters that show upgrade of cards
                thisVector[cardDict[thisCard]] += 1
            if (thisVector[136] == 1 and np.sum(thisVector) < 100):                  #check if "Ascenders Banes" is present: it should be, so remove deck if not.
                allVectors.append(thisVector.tolist())
            else:
                nmbrOutlierErrors += 1
        except KeyError:
            nmbrKeyErrors += 1
            errorCard.append(thisCard)
    
    with open(thisWriteFile, "w") as outFile:
        for vector in allVectors:
            strVector = []
            for i in range (len(vector)):
                strVector.append(str(int(vector[i])))
            outFile.write(" ".join(strVector) + "\n")
    
##  Store combined data in a seperate file

from toolbox.combineData import combineData
combineData(writeDir)






