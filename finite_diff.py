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


# Sample Inputs...

bounds = [  5, np.nan, np.nan, np.nan, 0,
            5, -1,     -1,     -1,     0,
            5, -1,     -1,     -1,     0,
            5, np.nan, np.nan, np.nan, 0]
condMap = []

rho = [     5, 0, 0, 0, 0,
            5, 0, 0, 0, 0,
            5, 0, 0, 0, 0,
            5, 0, 0, 0, 0]

G = GMatrix((5,4), bounds, condMap)

T = np.dot(np.linalg.inv(G),rho)

print(T)

TMap = []
# Remap Results
for l in range(0,4) :
    row = []
    for i in range(0,5) :
        row.append(T[l*5+i])
    TMap.append(row)


nx, ny = (5, 4)
x = np.linspace(0, 5, nx)
y = np.linspace(0, 4, ny)
xv, yv = np.meshgrid(x, y)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xv,yv,TMap,rstride=1, cstride=1, cmap=cm.coolwarm,
    linewidth=1, antialiased=False)
plt.show()
#plt.imshow(TMap, cmap='hot', interpolation='nearest')
#plt.show()
