from finite_diff import *
import numpy as np
from importImage import *

# Sample Inputs...

length = 1.5
width = 1

nLength = 60
nWidth = 40
bounds = importBounds('test60x40.png')
imagePath = 'trump-60x40.png'
condImage = importCondImage(imagePath,1e-4)
condDict = condMap(condImage)
  
rho = rhoVector(bounds)
G = GMatrix((nLength,nWidth), bounds, condDict)
T = np.dot(np.linalg.inv(G),rho)

plotPot(length,width,nLength,nWidth,T,imagePath)
plotField(length,width,nLength,nWidth,T)
plotJ(length,width,nLength,nWidth,T,condImage)



# plot the analytical solution
solXRes = 30
solYRes = 20
a = 1.0
b = 1.0
anaSol = np.zeros((solYRes,solXRes))

V = lambda x,y,n : (1.0/n)*(np.cosh(n*np.pi*x/a)/np.cosh(n*pi*b/a))*np.sin(n*np.pi*y/a)

for n in range(1,3,2) :
    for x in range(0,solXRes) :
        for y in range(0,solYRes) :
            anaSol[y,x] += V(2.0*x/(solXRes-1)-1.0,y/(solYRes-1),float(n))   
plot = []
for row in anaSol :
    for col in row :
        plot.append(col)

#plotPot(length,width,solXRes,solYRes,np.array(plot))
