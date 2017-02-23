import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# a Nan in the bounds sets the derivative to zero
def GMatrix(size, bounds, condMap):
    
    length = size[0]
    width = size[1]
    size = width*length
    G = np.zeros((size,size))

    # snake down left to right top down Y0...YN

    for i in range(0,size) :
        if(np.isnan(bounds[i])): # Zero derivative bound
            if(i < length) : # Top Boundry
                G[i][i] = -1
                G[i][i+length] = 1
            else : # Assume bottom bound because I'm lazy
                G[i][i] = -1
                G[i][i-length] = 1
        elif(bounds[i] != -1) :
            G[i][i] = 1
        else : # Not a B.C.
            G[i][i] = -4
            G[i][i-1] = 1
            G[i][i+1] = 1
            G[i][i-length] = 1
            G[i][i+length] = 1
            

    return(G)

def rhoVector(bounds):
    rho = []
    for bound in bounds :
        if np.isnan(bound) or bound == -1:
            rho.append(0)
        else :
            rho.append(bound)
    return rho

def plotField(length, width, nLength, nWidth, field):
    TMap = []
    # Remap Results
    for w in range(0,nWidth) :
        row = []
        for l in range(0,nLength) :
            row.append(field[w*nLength+l])
        TMap.append(row)

    nx, ny = (nLength, nWidth)
    x = np.linspace(0, length, nx)
    y = np.linspace(0, width, ny)
    xv, yv = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xv,yv,TMap,rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=1, antialiased=False)
    plt.show()

