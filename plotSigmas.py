"""
    Script specifically used to get a plot of the sigmas as used in the report.
     Note: This is not written to be efficient but to 'set and forget': when reusing on different data, I advice to test the separate datsets/settings seperatly in FindPCAs.py before using this!
"""

##  Imports, Constants, Names

#imports:
import os
os.chdir("C:/Users/merli/Documents/Data_Mining/")   #Don't know why this is required...
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.append("..")

#importing other scripts
import toolbox
from toolbox.cardDicts import classCardDict
from toolbox.cardDicts import toName
from toolbox.cardDicts import deckToNames
from toolbox.PCA import PCA
from toolbox.PCA import PCNormalise

#names of paths
here = "C:/Users/merli/Documents/Data_Mining/"

dirNameSilent = here+"FilteredDataSilent/"
dirNameIronclad = here+"FilteredData/"
fileNameSilent = dirNameSilent+"CombinedData.txt"
fileNameIronclad = dirNameIronclad+"CombinedData.txt"

#Constants
maxComp = 100
minSigma = 10


##Read decks

decksSilent = np.loadtxt(fileNameSilent, dtype=int, delimiter=" ")
decksIronclad = np.loadtxt(fileNameIronclad, dtype=int, delimiter=" ")
SigS =  PCA(decksSilent, output="Sigma", sparse =True, normalise=True, nmbrVectors=maxComp)
SigI =  PCA(decksIronclad, output="Sigma", sparse =True, normalise=True, nmbrVectors=maxComp)

##remove Strikes and defends


#code:

nmbrStCardsS = 4
nmbrStCardsI = 3

for i in range(len(decksSilent[:,1])):
    for j in range(nmbrStCardsS):
        decksSilent[i,j] = 0
for i in range(len(decksIronclad[:,1])):
    for j in range(nmbrStCardsI):
        decksIronclad[i,j] = 0

SigSWOSD =  PCA(decksSilent, output="Sigma", sparse =True, normalise=True, nmbrVectors=maxComp)
SigIWOSD =  PCA(decksIronclad, output="Sigma", sparse =True, normalise=True, nmbrVectors=maxComp)        


## rewrite Sigmas in terms of percentages

Sigs = [SigS, SigI, SigSWOSD, SigIWOSD]
for i in range(len(Sigs)):
    thisSum = np.sum(Sigs[i])
    Sigs[i] = np.cumsum(Sigs[i])
    for j in range(len(Sigs[i])):
        Sigs[i][j] = Sigs[i][j]/thisSum




## plot Sigma's


legend = ["Silent, with Starting cards", "Ironclad, with Starting cards","Silent, without Starting cards", "Ironclad, without Starting cards"]
sigFig = plt.figure()
for i in range(len(Sigs)):
    plt.plot(np.arange(1,len(Sigs[i])+1), Sigs[i])
plt.xlabel("number of PCs")
plt.ylabel("Information covered")
plt.title("Effect of adding Principle Components")
plt.legend(legend)
plt.show()






