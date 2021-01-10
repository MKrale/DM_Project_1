"""
    Provides the general functions to:
        find Sum of Square Errors (SSE's), 
        find good staring points for KMeans using 'Bisecting K-means'
"""
import numpy as np
import sklearn.metrics as sklMet
import sklearn.cluster as sklCl


def findMean(cluster):
    mean = []
    for i in range(len(cluster[0])):
        mean = np.append(mean, np.sum(cluster[:,i])/len(cluster))
    return mean
    
#finds the Sum of Square Error (SSE) of a cluster from centre
def findSSE(cluster, centre):    
    squaredErrors = 0
    for i in range(len(cluster)):
        squaredErrors += sklMet.mean_squared_error(centre,cluster[i])
    return squaredErrors
    
def BiKMeans(maxK, nmbrIterations, Data, minPer = 0.1, mindist=0.001, maxe = 25):
    #initialisation
    Clusters = np.ndarray(maxK, dtype=object)
    Clusters[0] = Data
    SSEs = np.array([1])
    AllPoints = np.ndarray(maxK, dtype=object)
    AllPoints[0] = np.ndarray( (1,len(Data[0])))
    bisect = sklCl.KMeans(2, n_init=1, max_iter = 1000)
    
    #main loop: find one new cluster
    for thisClusterNmbr in range(1,maxK):
        #print("doing cluster "+str(thisClusterNmbr))
        #find worst cluster
        thisClusterArg = np.argmax(SSEs)
        thisCluster = Clusters[thisClusterArg]
        #create points array
        thisPoints = np.ndarray( (thisClusterNmbr+1,len(Data[0])))
        for i in range(thisClusterNmbr):
            thisPoints[i] = AllPoints[thisClusterNmbr-1][i]
        #find Bisects
        allBisects = []
        for i in range(nmbrIterations):
            ValidFound = False
            j=0
            while (not ValidFound):  #checks wether enough points are put in both clusters -->might lead to problems!
                thisBisect = bisect.fit(thisCluster)
                ValidFound = isUsable(thisBisect, thisCluster, thisPoints[:-1], minPer, mindist, maxe)
                j += 1
                if (j>1000):
                    return ("ERROR: NO APROPRIATE CLUSTERS COULD BE FOUND (stuck at k="+str(thisClusterNmbr)+")")
            allBisects = np.append(allBisects, thisBisect)
        #chose best bisect --> other validation could be chosen!
        bestInertia = 10**1000
        bestI = -5
        for i in range(nmbrIterations):
            if (allBisects[i].inertia_ <= bestInertia):
                bestI = i
                bestInertia = allBisects[i].inertia_
        thisBisect = allBisects[bestI]
        #bisect -> clusters
        filter = thisBisect.labels_ == 0
        C1 = thisCluster[filter]
        C2 = thisCluster[np.logical_not(filter)]
        C1p, C2p =  thisBisect.cluster_centers_
        #save bisect correclty in Clusters, SSEs and points
        Clusters[thisClusterArg] = C1
        thisPoints [thisClusterArg] = C1p
        SSEs[thisClusterArg] = findSSE(C1, C1p)
        Clusters[thisClusterNmbr] = C2
        thisPoints[thisClusterNmbr] = C2p
        SSEs = np.append(SSEs, findSSE(C2, C2p))
        AllPoints[thisClusterNmbr] = thisPoints
    
    return AllPoints
    
def isUsable(thisBisect, thisCluster, thisPoints, minPer, mindist, maxe):
    #check min and max number of points
    nmbrPoints = (np.sum(thisBisect.labels_))
    low, up = len(thisCluster)*minPer, len(thisCluster)*(1-minPer)
    if (not ( nmbrPoints > low and nmbrPoints < up)):
        return False
    #check if point is too close to existing one
    C1, C2 = thisBisect.cluster_centers_
    if (np.sum(np.abs(C1-C2)) <mindist):
        print("too close1")
        return false
    else:
        for i in range(len(thisPoints)):
            if  (np.sum(np.abs(C1-thisPoints[i])) <mindist):
                return False
            elif (np.sum(np.abs(C2-thisPoints[i])) <mindist):
                return False
    #check if no values are extremely high or all too low
    if ((np.max(np.abs(C1)) + np.max(np.abs(C2))) > 10**maxe):
        return False
    elif (np.sum(np.abs(C1)) < mindist or np.sum(np.abs(C2)) < mindist):
        return False
    return True