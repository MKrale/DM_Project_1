"""
    Script specifically used to get a plot of the SSEs as used in the report.
     Note: This is not written to be efficient but to 'set and forget': when reusing on different data, I advice to test the separate datsets/settings seperatly in FindClusters.py before using this!
"""

#constants
#thisClass = 'Ironclad'
thisClass = 'Silent'
maxK =25
nmbrIterations = 10

usePCs = False
withSD = False
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
dirNameS = here+"FilteredDataSilent/"

dirNameI = here+"FilteredData/"
fileNameS = dirNameS+"CombinedData.txt"
fileNameI = dirNameI+"CombinedData.txt"

#names of in- and outputfiles
endingI25 = str(25)+".txt"
endingS25 = "Silent"+str(25)+".txt"
endingI10 = str(10)+".txt"
endingS10 = "Silent"+str(10)+".txt"

allDataFiles = [dirName+"PCAData"+endingI10, dirName+"PCAData"+endingS10,dirName+"PCAData"+endingI25, dirName+"PCAData"+endingS25, fileNameI, fileNameS]


#Ignoring WSD's, since they causes an error
## importing data
KMeans = []
SSEs = np.ndarray(len(allDataFiles), dtype=object)

for i in range(len(allDataFiles)):
    print("Doing "+allDataFiles[i])
    thisSSE = []
    thisData = np.loadtxt(allDataFiles[i])
    clusterStartPoints = BiKMeans(maxK, nmbrIterations, thisData)
    for j in range(maxK):
        thisSSE.append(sklCl.KMeans(n_clusters = j+1, init = clusterStartPoints[j], n_init = 1).fit(thisData).inertia_)
    SSEs[i] = thisSSE
## Normalising

for i in range(len(SSEs)):
    thisMax = SSEs[i][0]
    for j in range(len(SSEs[i])):
        SSEs[i][j] = SSEs[i][j] / thisMax

## Calculate starting clusterpoints using function from toolbox

legend = ["Ironclad, 10 PCs", "Silent, 10 PCs","Ironclad, 25 PCs", "Silent, 25 PCs","Ironclad, unprocessed", "Silent, unprocessed"]
sigFig = plt.figure()
for i in range(len(SSEs)):
    plt.plot(np.arange(1,len(SSEs[i])+1), SSEs[i])
plt.xlabel("Number of Clusters")
plt.ylabel("SSE / maximum SSE")
plt.title("Sum of Squared Error for different Clusterings")
plt.legend(legend)
plt.show()










