"""
    Finds Clusters for decks with a Bisecting K-means algorithm
     1)reading the data produced by ReadFile.py
     2)find the principal components of these decks
     3)rewrite decks in terms of principal components with high contributions.
"""

## Constants, imports, etc.

#constants
#thisClass = 'Ironclad'
thisClass = 'Silent'
maxK = 10
nmbrIterations = 50

usePCs = True
withSD = False
nbmrPCs = 25
nmbrCards = 149

analyse = True

#imports:
import os
os.chdir("C:/Users/merli/Documents/Data_Mining/")   #Don't know why this is required...
import numpy as np
import sys
sys.path.append("..")
import sklearn.metrics as sklMet
import sklearn.cluster as sklCl
import matplotlib.pyplot as plt
#importing other scripts
import toolbox
from toolbox.cardDicts import classCardDict
from toolbox.cardDicts import toName
from toolbox.cardDicts import deckToNames
from toolbox.PCA import PCA
from toolbox.PCA import fromPCs
from toolbox.PCA import typicalDeck
from toolbox.bisectingKMeans import BiKMeans

#names of paths
here = "C:/Users/merli/Documents/Data_Mining/"
dirName = here+"PCAData/"

writeDirName = here+"ClusterData/"
if (thisClass == 'Silent'):
    rawDirName = here+"FilteredDataSilent/"
elif (thisClass == 'Ironclad'):
    rawDirName = here+"FilteredData/"
rawDatafileName = rawDirName+"CombinedData.txt"

#names of in- and outputfiles
if withSD:
    ending = str(nbmrPCs)+"_withSD.txt"
else:
    ending = str(nbmrPCs)+".txt"
if (thisClass == 'Silent'):
    ending = 'Silent'+ending
    
dataFileName = dirName+"PCAData"+ending
vFileName = dirName+"PCAComps"+ending

writeFilePoints = writeDirName+"clusterPoints"+ending
## importing data

if usePCs:
    PCDecks = np.loadtxt(dataFileName, dtype=float, delimiter=" ")
    PCs = np.reshape(np.loadtxt(vFileName, dtype=float, delimiter=" "), (nbmrPCs,-1))
else:
    PCDecks = np.loadtxt(rawDatafileName, dtype=int, delimiter=" ")
    if (not withSD):
        if (thisClass == 'Silent'):
            nmbrStCards = 4
        elif (thisClass == 'Ironclad'):
            nmbrStCards = 3
    
        for i in range(len(PCDecks[:,1])):
            for j in range(nmbrStCards):
                PCDecks[i,j] = 0
## Calculate starting clusterpoints using function from toolbox

clusterStartPoints = BiKMeans(maxK, nmbrIterations, PCDecks)

## Save clusterpoints
with open(writeFilePoints, "w") as outFile:
    for thisK in clusterStartPoints:
        for thisPoint in thisK:
            strVector = []
            for i in range (len(thisPoint)):
                strVector.append(str(thisPoint[i]))
            outFile.write(" ".join(strVector) + "\n")
##

## plot SSE and d_SSE for different k's to determine right number of clusters.

if analyse:
    SSEs = []
    KMeans = []
    
    for i in range(maxK):
        KMeans.append(sklCl.KMeans(n_clusters = i+1, init = clusterStartPoints[i], n_init = 1).fit(PCDecks))
        SSEs.append(KMeans[i].inertia_)
    maxSSE = np.max(SSEs)
    plotSSE = plt.figure()
    plt.plot(np.arange(1, maxK+1), SSEs)
    plt.title("SSE for different k's")
    plt.xlabel("number of clusters k")
    plt.ylabel("SSE")
    plt.axis([0,10,0,maxSSE])
    plt.figtext(0.1, -0.05, "Sum of Squared Error (SSE) for different numbers of clusters. Using decks rewritten in 25 Principal Components.")
    plt.show()
    
    
    d_SSEs = []
    for i in range(1,maxK):
        d_SSEs.append(SSEs[i-1] - SSEs[i] )
    
    plotDSSE = plt.figure()
    plt.plot(np.arange(2, maxK+1), d_SSEs)
    plt.title("Decrease of SSE for different k's")
    plt.xlabel("number of clusters k")
    plt.ylabel("Loss in SSE")
    #plt.axis([0,10,0,15000])
    plt.figtext(0.1, -0.05, "Decrease of Sum of Squared Error (SSE) for differnt number of clusters. Using decks rewritten in 25 Principal Components")
    
    plt.show()
## show highest absolute values per centre point
    #constants
    nmbrCards = 10
    k = 9
    minN = 0.000001
    #code
    for i in range(k):
        thisP = np.absolute(fromPCs (KMeans[k].cluster_centers_[i], PCs))
        print(" \nCluster "+str(i+1)+"'s most important cards:")
        for j in range(nmbrCards):
            maxArg = np.argmax(thisP)
            thisCard =toName(maxArg, thisClass)
            n = fromPCs (KMeans[k].cluster_centers_[i], PCs)[maxArg]
            if (np.abs(n)>minN):
                print(str(j)+": "+thisCard+", n="+str(n))
            thisP[maxArg] = 0
## convert clusters for given k into 'typical decklists'
    k = 4
    if usePCs:
        for i in range(k):
            print("\n Cluster "+str(i+1)+" of "+str(k)+":")
            deckToNames(typicalDeck(fromPCs (KMeans[k].cluster_centers_[i], PCs), useStartingCards = withSD), thisClass)
    else:
        for i in range(k):
            print("\n Cluster "+str(i+1)+" of "+str(k)+":")
            deckToNames(typicalDeck(KMeans[k].cluster_centers_[i], useStartingCards = withSD), thisClass)

    


















