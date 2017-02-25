from finite_diff import *
import numpy as np
from importImage import *

# Sample Inputs...

length = 1.5
width = 1
nLength = 30
nWidth = 20
bounds = importBounds('gnd_sides_30x20.png')
imagePath = 'bottle_30x20.png'
condImage = importCondImage(imagePath,1e-3)
condDict = condMap(condImage)
  
rho = rhoVector(bounds)
G = GMatrix((nLength,nWidth), bounds, condDict)
T = np.dot(np.linalg.inv(G),rho)
 
plotField(length,width,nLength,nWidth,T,imagePath)

