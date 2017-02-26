import matplotlib.pyplot as plt
from scipy import misc
from pylab import *
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png


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
                G[i][i] = -1.0
                G[i][i+length] = 1.0
            else : # Assume bottom bound because I'm lazy
                G[i][i] = -1.0
                G[i][i-length] = 1.0
        elif(bounds[i] != -1) : # It is a source
            G[i][i] = 1
        else : # Not a B.C.
            G[i][i] = -(condMap[i,i-1]+condMap[i,i+1]+condMap[i,i-length]+condMap[i,i+length])
            G[i][i-1] = condMap[i,i-1]
            G[i][i+1] = condMap[i,i+1]
            G[i][i-length] = condMap[i,i-length]
            G[i][i+length] = condMap[i,i+length]
            

    return(G)

def condMap(image):
    condDict = {}

    length = len(image[0])
    
    for row in range(0,len(image)) :
        for col in range (0,len(image[0])) :
            upIndex = coordToInd(col,row-1, length)
            downIndex = coordToInd(col,row+1, length)
            centerIndex = coordToInd(col,row, length)
            leftIndex = coordToInd(col-1,row, length)
            rightIndex = coordToInd(col+1,row, length)

            # Assign top bottom conductivity
            if (row < len(image) - 1) : # There are items below
                condDict[centerIndex,downIndex] = max(image[row][col],image[row+1,col])
            if (row > 0) : # There are items above
                condDict[centerIndex,upIndex] = max(image[row][col],image[row-1,col])

            # Assign left right conductivity
            if (col < len(image[0]) - 1) : # There are items to the right
                condDict[centerIndex,rightIndex] = max(image[row][col],image[row,col+1])
            if (col > 0) : # There are items to the left
                condDict[centerIndex,leftIndex] = max(image[row][col],image[row,col-1])

    return condDict
                

def coordToInd(x, y, length) :
    return y*length + x

def rhoVector(bounds):
    rho = []
    for bound in bounds :
        if np.isnan(bound) or bound == -1:
            rho.append(0)
        else :
            rho.append(bound)
    return rho

def plotPot(length, width, nLength, nWidth, field, imPath = ''):
    

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
    ax.set_title("Potential in x and y")
    ax.plot_surface(xv,yv,TMap,rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=1, antialiased=False)
    ax = gca(projection='3d')
    if imPath != '' :
        img = misc.imread(imPath)/255.0
        ax.plot_surface(xv, yv, -1, rstride=1, cstride=1, facecolors=img)
    plt.show()

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

    u,v = np.gradient(TMap)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Potential in x and y")
    ax.quiver(xv,yv,-1*v,-1*u)
    plt.show()


def plotJ(length, width, nLength, nWidth, field, condMap):
    
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

    # Gradient of potential multiplied by the conductivity at that point 
    u,v = np.gradient(np.multiply(TMap,condMap))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Potential in x and y")
    ax.quiver(xv,yv,-1*v,-1*u)
    plt.show()
