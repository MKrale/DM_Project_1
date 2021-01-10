"""
    Finds PCA of decks by:
     1)reading the data produced by ReadFile.py
     2)find the principal components of these decks
     3)rewrite decks in terms of principal components with high contributions.
     4)Code to visulalise the PCA's
"""

##  Imports, Constants, Names
#Constants
thisClass = 'Silent'
#thisClass = 'Ironclad'
maxComp = 25
minSigma = 10
withSD = False
analyse = True

#imports:
import os
os.chdir("C:/Users/merli/Documents/Data_Mining/")   #Don't know why this is required...
import numpy as np
import sys
sys.path.append("..")

#importing other scripts
import toolbox
from toolbox.cardDicts import classCardDict
from toolbox.cardDicts import toName
from toolbox.cardDicts import deckToNames
from toolbox.PCA import PCA
from toolbox.PCA import PCNormalise
from toolbox.PCA import typicalDeck

#names of paths
here = "C:/Users/merli/Documents/Data_Mining/"
if (thisClass == 'Silent'):
    dirName = here+"FilteredDataSilent/"
elif (thisClass == 'Ironclad'):
    dirName = here+"FilteredData/"
fileName = dirName+"CombinedData.txt"
writeDirName = here+"PCAData/"

#making filenames using constants
if withSD:
    ending = str(maxComp)+"_withSD.txt"
else:
    ending = str(maxComp)+".txt"
if (thisClass == 'Silent'):
    ending = 'Silent'+ending


writeFileData = writeDirName+"PCAData"+ending
writeFileComps = writeDirName+"PCAComps"+ending

##Read decks

decks = np.loadtxt(fileName, dtype=int, delimiter=" ")

##optional: remove Strikes and defends

#constants:

#code:
if (not withSD):
    if (thisClass == 'Silent'):
        nmbrStCards = 4
    elif (thisClass == 'Ironclad'):
        nmbrStCards = 3

    for i in range(len(decks[:,1])):
        for j in range(nmbrStCards):
            decks[i,j] = 0
        
## apply PCA, keep specified number of components
#decks = decks[:,:-13]           #removing curses: from testing, these seem to not matter.t
PCDecks, means, Sig, V = PCA(decks, output="All", sparse =True, normalise=True, nmbrVectors=maxComp)

#remove components
#maxComp = 0
#while Sig[maxComp] > minSigma:
#    maxComp += 1                   #find components that have sigma>minSigma: not used
PCADecks = PCDecks[:,:maxComp]
PCAComps = V[:maxComp]            #should do nothing if sparse PCA function is used.

#save in files
np.savetxt(writeFileData, PCADecks)
np.savetxt(writeFileComps, PCAComps)

## print most important cards for first PC's

if analyse:
    #constants
    nmbrCards = 10
    nmbrVCAs = 5
    minN = 0.000001
    #code
    for i in range(nmbrVCAs):
        thisPCA = np.absolute(V[i])
        print(" \nPCA "+str(i+1)+"'s most important cards:")
        for j in range(nmbrCards):
            maxArg = np.argmax(thisPCA)
            thisCard =toName(maxArg, thisClass)
            n = V[i,maxArg]
            if (np.abs(n)>minN):
                print(str(j)+": "+thisCard+", n="+str(n))
            thisPCA[maxArg] = 0
##
    for i in range (nmbrVCAs):
        print(" \n PCA "+str(i+1)+" typical Deck:")
        deckToNames(typicalDeck(V[i], useStartingCards= withSD), thisClass)
        print(" \n Inverse:")
        deckToNames(typicalDeck(V[i], useStartingCards= withSD), thisClass)

## Plot decks according to PC's
    import matplotlib.pyplot as plt
    #constants:
    maxPCA = 4
    nmbrDecks = len(PCADecks[:,1])
    ptsize = (1/maxPCA)
    #code:
    f, ax = plt.subplots(maxPCA, maxPCA)
    for i in range(maxPCA):
        for j in range(maxPCA):
            if (i!=j):
                ax[j,i].scatter(PCADecks[:nmbrDecks,i], PCADecks[:nmbrDecks,j], 0.5)
            if (j==0):
                ax[i,j].set_ylabel("PC "+str(i+1))
            if (i==(maxPCA-1)):
                ax[i,j].set_xlabel("PC "+str(j+1))
    plt.show()

## 3D plot of first three PCs
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure()
    ax2 = fig.add_subplot(111,projection='3d')
    ax2.scatter(PCADecks[:,0],PCADecks[:,1],PCADecks[:,2], s=0.5)
    ax2.set_xlabel("First PC")
    ax2.set_ylabel("Second PC")
    ax2.set_zlabel("Third PC")
    
    plt.show()
    
## Plot Sigma for PC's

    SigPlot = plt.figure()
    

##  Testing/visualisation Functions

def checkPCs(pcs, minval = 10**-2):
    interestingCards = []
    for i in range(len(pcs[0])):
        b = True
        j=0
        while (b and j<len(pcs)):
            if (abs(pcs[j,i])>minval):
                b=False
                interestingCards.append(i)
            j += 1
    return interestingCards









