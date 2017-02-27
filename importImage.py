import numpy as np
from scipy import misc

def importBounds(filename) :
    image = misc.imread(filename)
    bounds = []
    for row in image :
        for pixel in row :
            if pixel[0] == 0 and pixel[1] == 255 and pixel[2] == 0: # pixel is green
                bounds.append(np.nan)
            elif pixel[0] > 0 or pixel[2] > 0: # pixel is red to blue
                bounds.append((255-pixel[2]+pixel[0])/510)
            else :
                bounds.append(-1)
    return bounds

def importCondImage(filename, minSigma) :
    image = np.array(misc.imread(filename, flatten = True))
    image = np.flipud(image)
    maxValue = image.max()
    offset = (minSigma*maxValue)/(1-minSigma)
    
    return (image + offset-image.min()) / (maxValue + offset-image.min())

#    return(image)/(maxValue)
    
