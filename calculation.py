import numpy as np



def filetoarray(datfile):
    airfoildat1 = [] #upper surface
    airfoildat2 = [] #lower surface
    with open(datfile,'r') as dat:
       
        for row in dat:
            t = row.rstrip().lstrip()
            v = t.split(' ')
            if '' in v: #to get the space 
                del v[v.index('')]
                
            for i in range(len(v)):
                v[i] = float(v[i])
                
            airfoildat1.append(v)
        
    index = airfoildat1.index([])
    temp = airfoildat1.copy()
    
    airfoildat2 = np.array(temp[index+1:])
    airfoildat1 = np.array(airfoildat1[1:index]) #removing the second set of zeros
    
    airfoildat1 = np.flip(airfoildat1,0) #flipping so that starting point is TE
    
    airfoildat = np.concatenate((airfoildat1,airfoildat2))
    
    return airfoildat #return airfoildat

r = filetoarray('test.txt')
#print(r)

def discretize(airfoildat): #returns descretedat
    n = len(airfoildat)
    x_list = []
    y_list = []
    
    for i in range(n-1):
        tmpx = [airfoildat[i,0],airfoildat[i + 1,0]] #making segment
        tmpy = [airfoildat[i,1],airfoildat[i + 1,1]]
        x_list.append(tmpx)
        y_list.append(tmpy)
        
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    discretedat = np.array([x_list,y_list])
    
    return discretedat 
    
k = discretize(r)
print(k)


def KuttaCondition(discretedat):#enforces kutta condition (gamma(TE) = 0)
    #determinng TE type (cusped or finite); my train of thought: if both segment 'vectors' point in the same general direction, the TE is cusped
    upper_vec = (discretedat[1,0,0] - discretedat[1,0,1]) / (discretedat[0,0,0] - discretedat[0,0,1])
    lower_vec = (discretedat[1,-1,0] - discretedat[1,-1,1]) / (discretedat[0,-1,0] - discretedat[0,-1,1])

    cusped = False
    if np.sign(upper_vec) == np.sign(lower_vec): #cusped = True
        cusped = True
    else: #cusped = False
        cusped = False
    
    return cusped
    

            
def vortexMethod(aoa,V_inf,discretedat):
    