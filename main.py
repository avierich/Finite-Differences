from finite_diff import *
import numpy as np
from importImage import *

# Sample Inputs...

length = 1.5
width = 1
nLength = 30
nWidth = 20
bounds = importBounds('funky_30x20.png')
condMap = []
  
rho = rhoVector(bounds)
G = GMatrix((nLength,nWidth), bounds, condMap)
T = np.dot(np.linalg.inv(G),rho)
 
plotField(length,width,nLength,nWidth,T)

