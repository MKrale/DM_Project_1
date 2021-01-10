"""
    Defines the function PCA, which finds the principal components of the given Data and outputs
    
"""
#imports
import numpy as np
import numpy.linalg as ln
import scipy.sparse.linalg as sln

#function
def PCA(Data, output="Data", sparse = "False", normalise = "False", nmbrVectors = 10):
    means = np.mean(Data, axis = 0)
    Data = np.array(Data - means, dtype = float)
    if normalise:
        Data = PCNormalise(Data)
    
    if sparse:
        U_, Sig_, V_ = sln.svds(Data, k=nmbrVectors)
        order = np.argsort(Sig_)#sort according to Sig's
        Sig = Sig_[order[::-1]]
        V = V_[order[::-1]]
        Data = np.dot(Data, np.transpose(V))
    else:
        U, Sig, V = ln.svd(Data)
        Data = np.dot(Data, np.transpose(V))
    if output == "Data":
        return Data
    elif output == "means":
        return means
    elif output =="Sigma":
        return Sig
    elif output =="V":
        return V
    elif output =="All":
        return [Data, means, Sig, V]

def PCNormalise(Data):
    for i in range (len(Data[1])):
        thismax = np.max(Data[:,i])
        if (thismax !=0):
            np.true_divide(Data[:,i], thismax, out = Data[:,i])
    return Data

def fromPCs(Pdata, V):
    return np.dot(Pdata,V)

#Visulatation function: outputs a 'most likely deck' given a PCA
def typicalDeck(V, nmbrCards = 25, inv = False, useStartingCards = True):
    if (not useStartingCards):
        V[0] = 0
        V[1] = 0
    normalFactor = np.sum(np.abs(V))
    deck = np.zeros(len(V))
    typCardArg = np.argmax(np.abs(V))
    if ((V[typCardArg] <0 and not inv) or (V[typCardArg] >0 and inv)):
        for i in range(len(V)):
            V[i] = -V[i]
    for i in range (nmbrCards):
        thisCardArg = np.argmax(V)
        deck[thisCardArg] = deck[thisCardArg]+1
        V[thisCardArg] = V[thisCardArg] - (normalFactor/nmbrCards)
    return deck