import numpy as np
from copy import deepcopy


def main(s,r):
    size, radius = s, r

    
    A = np.zeros((size,size, size)) 

    AA = deepcopy(A) 
    x0, y0, z0 = int(np.floor(A.shape[0]/2)), \
            int(np.floor(A.shape[1]/2)), int(np.floor(A.shape[2]/2))
    positions=[]

    for x in range(x0-radius, x0+radius+1):
        for y in range(y0-radius, y0+radius+1):
            for z in range(z0-radius, z0+radius+1):
             
                deb = radius - abs(x0-x) - abs(y0-y) - abs(z0-z) 
                if (deb)==0: 
                    AA[x,y,z] = 1
                    positions.append([x,y,z])


    return AA,positions