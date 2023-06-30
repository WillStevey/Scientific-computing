# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:52:14 2021
Traffic simulation function code
@author: Wstev
"""
import numpy as np
import matplotlib.pyplot as plt

"""
General paremeters - The traffic simulation is characterised by 7 different paremters; lanes,s,tmax,vmax,N,psl,psp,po
    lanes - number of individual roads that make up the highway, this is how many rows the road matrix L will have
    s - length of the array L which represents the road
    tmax - the number of timesteps the code will run for
    vmax - the maximum speed allowed on the road
    N - the initial number of cars on the road
    psl - the probability a car will slow down
    psp - the probability a car will speed by exceeding vmax if it is travelling at a speed of vmax
    po - the probability that a car will overtake (swapping lanes) if it is travelling slow enough,not applicable for single lane systems

   -In the code some variables are used multiple times; L,usefuln,r
   L - a 2D array that represents a series of straight roads parallel to each other with its dimensions described by parameters lanes,s
   usefuln - the current positions of the cars at any timestep,it is calculated once each timestep and passed into the other functions
   r - the index describing each lane eg r = 1 is the first lane
"""

"""
Basic functions
"""

"""
Inputs : L,r 
Use : Finds the positions of the cars along L
Outputs : usefuln
"""

def carpositions(L,r):      
    usefuln = np.array([])
    n = 0          # counter used for loop
    s = len(L[0,0:])
    while n < s:
        if L[r,n] != None:          #Finds all not None values in the array these are the postions of the care
            usefuln = np.append(usefuln,n)
        n = n + 1
    
    return usefuln

"""
Inputs : usefuln,L,r,vmax
Use : any car which has speed < vmax will accellerate by 1
Outputs : none
"""
def accelleration(usefuln,L,r,vmax):
    l = 0
    while l < len(usefuln) :
        g = int(usefuln[l])
        if L[r,g] < vmax:
            L[r,g] = L[r,g] + 1
        l = l + 1

"""
Inputs : usefuln,L,r,vmax
Use : The function will check for each car whether there are any cars in front of it,
if there are the car will slow down,how quickly depending on how close it is to the car infront of it
Outputs : none
"""       
def braking(usefuln,L,r,vmax):
    l = 0
    s = len(L[0,0:])
    while l < len(usefuln):
        g = int(usefuln[l])
        nearbycar = True
        n = g
        j = 1
        while nearbycar == True:
            d = j + n
            if d < s:   
                if L[r,n+j] != None:
                    if L[r,g] > (j - 1):
                        L[r,g] = j - 1
                        nearbycar = False                         
                                   
            if d >= s:         
                if L[r,d-s] != None:
                    if L[r,g] > (j - 1):
                        L[r,g] = j - 1      #Instead
                        nearbycar = False
                            
                      
            if j > vmax:
                nearbycar = False
            j = j +1 
        l = l + 1

"""
Inputs : usefuln,L,r,ps
Use : Cars may now randomly slow down
Outputs : none
"""
def random(usefuln,L,r,ps):    
    l = 0
    while l < len(usefuln):
        g = int(usefuln[l])               
        n = g
        a = np.random.rand(1)         #this generates a random number between 1 and 0 to compare with the probability
        if a < ps:
            if L[r,n] > 0:
                L[r,n] = L[r,n] - 1
        l = l + 1

"""
Inputs : L,r,t(the current timestep),lanes
Use : Displaces all the cars according to their speed and counts how may reach the end of the road
Outputs :L (an array containing the new postions of the cars after one iteration of the loop) and
q1 (the number of cars that loop around to the start of the road)
"""

def displacement(L,r,t,lanes):
    global q1
    usefuln = carpositions(L,r)
    r = int(r)
    l = 0
    s = len(L[0,0:])
    L1 = np.full([lanes,s], None) 
    t = t
    tcutoff = 10*s
    while l < len(usefuln):
           
        g = int(usefuln[l])
        n = g
        d = L[r,n] + n   # this is the displacement of the car
        if d < s:                         #this displaces each car if they do not reach the end of the road
            q = d 
            L1[r,q] = L[r,n]                  #the new displacements of all the cars are stored in a dummy array
            L[r,n] = None                      #The old position of the car is left empty
            
            
        if d >= s:                               #This part loops the cars back to the start of the road when they would leave it
            q = d - s
            if t > tcutoff:
                q1 = q1 + 1
                #print("flow")
                
            L1[r,q] = L[r,n]
            L[r,n] = None
        l = l + 1        
    L[r,0:s] = L1[r,0:s]    
    
    return L,q1
"""
Inputs : none
Use : Starts a counter to measure the flow rate
Outputs : None
"""
def startcount(q):
    global q1
    q1 = 0    

"""
Inputs : L,r,usefuln
Use : Plots usefuln against r, can be used for animations that ivolve multiple lanes
Outputs : None
"""

def plotting(usefuln,L,r):
    g = usefuln
    s = len(L[1,0:])
    plt.xlim(0,s)
    plt.ylim(0,5)
    plt.plot(g,np.ones(len(g))*(r+0.5),"*")     #this plots the positions of the cars                     
    plt.pause(0.1)


"""
Inputs : L,r,usefuln,t,tmax
Use : Plots usefuln against t, can be used to produce timespace plots
Outputs : None
"""
def timespaceplot(usefuln,L,r,t,tmax,s):
    g = usefuln
    
    plt.xlim(0,s)
    plt.ylim(10*s,tmax)
    if t > 10*s:
        plt.plot(g,np.ones(len(g))*t,"rx")     #this plots the positions of the cars   remove transient period                  
    plt.pause(0.1)
    
"""
Inputs : L,r,usefuln,vmax,psp
Use : Drivers that are drving at vmax have a chance of speeding, leading to speeds above the allowed
Outputs : None
"""
def speeding(usefuln,L,r,vmax,psp):
    
    l = 0
                      
    while l < len(usefuln):
        g = int(usefuln[l])
        n = g
        a = np.random.rand(1)        #this codes is almost identical to the random slowing code
        if a < psp:
            if L[r,n] > vmax:
                L[r,n] = L[r,n] + 1
        l = l + 1

"""
Inputs : L,r,usefuln,po,lanes
Use : When they are multiple lanes drivers have the chance of switching roads and overtaking, two functions one for drivers
going left, r to r + 1 and one for drivers going right, r to r - 1
Outputs : None
"""
def overtakingl(usefuln,L,r,po,lanes):
    l = 0
    while l < len(usefuln):
        if r == (lanes-1):
            break
        g = int(usefuln[l])
        n = g
        if L[r,n] == 0:
            a = np.random.rand(1)
            if a < po:
                if L[r+1,n] == None:                       #if an adjacent spot in an array is empty the car will switch lanes,
                    L[r+1,n] = L[r,n]
                    L[r,n] = None
                    
        l = l + 1
                    
def overtakingr(usefuln,L,r,po):
    l = 0
    while l < len(usefuln):
        if r == (0):
            break
        g = int(usefuln[l])
        n = g
        if L[r,n] == 2:
            a = np.random.rand(1)
            if a < po:
                if L[r-1,n] == None:
                    L[r-1,n] = L[r,n]
                    L[r,n] = None
                    
        l = l + 1                    

"""
Inputs : L,r,it(an integer used to find the amount of time needed to be cut off),lanes
Use : Displaces all the cars according to their speed
Outputs :L (an array containing the new postions of the cars after one iteration of the loop) and
q1 (the number of cars that loop around to the start of the road)
"""


def displacementintialtransient(L,r,t,lanes,it):
    global q1
    usefuln = carpositions(L,r)
    r = int(r)
    l = 0
    s = len(L[0,0:])
    L1 = np.full([lanes,s], None) 
    t = t
    tcutoff = it*s            # This sets how many points must be discounted to remove the initial transient behaviour of the simulation
    while l < len(usefuln):
           
        g = int(usefuln[l])
        n = g
        d = L[r,n] + n   # this is the displacement of the car
        if d < s:                         #this displaces each car if they do not reach the end of the road
            q = d 
            L1[r,q] = L[r,n]                  #the new displacements of all the cars are stored in a dummy array
            L[r,n] = None                      #The old position of the car is left empty
            
            
        if d >= s:                               #This part loops the cars back to the start of the road
            q = d - s
            if t > tcutoff:
                q1 = q1 + 1
                #print("flow")
                
            L1[r,q] = L[r,n]
            L[r,n] = None
        l = l + 1        
    L[r,0:s] = L1[r,0:s]    
    
    return L,q1

"""
Inputs : L,r,t,vmax,tmax,psl,psp,po,s,lanes
Use : Calls all the functions in order for each step of the algorithm
Outputs :flowrate (the number of cars that have looped round the array divided by the timesteps minus the initial transient period)
"""

def multiovertaking(L,r,t,vmax,tmax,psl,psp,po,s,lanes):   #This is acombination of all the functions
    v = carpositions(L,r)
    accelleration(v,L,r,vmax)
    braking(v,L,r,vmax)
    random(v,L,r,psl)
    speeding(v,L,r,vmax,psp)
    overtakingl(v,L,r,po,lanes)
    overtakingr(v,L,r,po)
    flow = displacement(L,r,t,lanes)
    flowrate = flow[1]/(tmax-10*s)
    
    return flowrate

"""
Inputs : L,lanes,t,vmax,tmax,psl,psp,po,s
Use : Calls multiovertaking for each lane
Outputs : The total flow from all the lanes together
"""

def multitrafficovertaking(L,lanes,t,vmax,tmax,psl,psp,po,s):  #this finds the flow
    roads = np.arange(0,(lanes))
    n = 0
    multiflow = 0
    while n < lanes:   #This calls multiovertaking for each row of L
        multiflow = multiflow + multiovertaking(L,roads[n],t,vmax,tmax,psl,psp,po,s,lanes)
        n = n + 1
    
    return multiflow   

"""
Inputs : L,r,t,vmax,tmax,psl,psp,po,s,lanes,it
Use : Calls all the functions in order for each step of the algorithm but instead allows the initial transient time to be modified
Outputs : flowrate
"""
def multiovertakinginitialtransient(L,r,t,vmax,tmax,psl,psp,po,s,lanes,it):
    v = carpositions(L,r)
    accelleration(v,L,r,vmax)
    braking(v,L,r,vmax)
    random(v,L,r,psl)
    overtakingl(v,L,r,po,lanes)
    overtakingr(v,L,r,po)
    flow = displacementintialtransient(L,r,t,lanes,it)
    flowrate = flow[1]/(tmax-it*s)
    
    return flowrate

"""
Inputs : L,lanes,t,vmax,tmax,psl,psp,po,s,it
Use : Calls multiovertakinginitialtransient for each lane
Outputs : The number of cars that have looped round the array
"""
def multitrafficovertakinginitialtransient(L,lanes,t,vmax,tmax,psl,psp,po,s,it):  #this finds the flow
    roads = np.arange(0,(lanes))
    n = 0
    multiflow = 0
    while n < lanes:
        multiflow = multiflow + multiovertakinginitialtransient(L,roads[n],t,vmax,tmax,psl,psp,po,s,lanes,it)
        n = n + 1
    
    return multiflow  
 
"""
Inputs : lanes,s,N
Use : Creates and fills an empty set of roads with N cars starting from position 0 on the array 
Outputs : A filled array of with a numner of rows equal to the value of lanes with each row being of length s and filled with N cars
"""

def fillroad(lanes,s,N):
    L = np.full(shape = (lanes,s), fill_value = None)    #generates the motorway from the number of lanes and the road length
    n = 0
    while n < lanes:         #write function that fills each lanes with N cars from the start of the array
        L[n,0:N] = 0
        n = n + 1
    return L

"""
Inputs : lanes,s,tmax,vmax,N,psl,psp,po
Use: Varies the density of cars by altering N and keeping s constant
Outputs : an array of flowrates and corresponding density's
"""

def Traffic(lanes,s,tmax,vmax,N,psl,psp,po):
       #generates the motorway from the number of lanes and the road length
    #lanes = lanes + 1 #this is due to make sure the indices line up
    L = fillroad(lanes,s,N)
    
    flowratestorage = np.array([])  # These are empty arrays to store values for density and flowrate in
    densitystorage =  np.array([])
    
    while N < 0.3*s:
        L = fillroad(lanes,s,N)
        totalflow = 0
        t = 0
        startcount(0)
        while t < tmax:
            flow = multitrafficovertaking(L,lanes,t,vmax,tmax,psl,psp,po,s)
            totalflow = totalflow + flow
              
            t = t + 1  
        
        flowrate = totalflow/(tmax-10*s)   #this finds the flow rate by dividing by the timesteps where the flow was being counted
        density = N/s
        densitystorage = np.append(densitystorage,density)
        flowratestorage = np.append(flowratestorage,flowrate)
        N = N + 1    
    return flowratestorage,densitystorage  

"Functions used for investigations"       

"This is used to vary vmax whilst keeping density constant"

def Vmaxinvestigation(lanes,s,tmax,vmax,N,psl,psp,po):
    L = fillroad(lanes,s,N)
    flowratestorage = np.array([]) 
    while vmax < 30:
        L = fillroad(lanes,s,N)
        totalflow = 0
        t = 0
        startcount(0)
        while t < tmax:
            flow = multitrafficovertaking(L,lanes,t,vmax,tmax,psl,psp,po,s)
            totalflow = totalflow + flow
              
            t = t + 1  
        flowrate = totalflow/(tmax-10*s) 
        flowratestorage = np.append(flowratestorage,flowrate)
        
        vmax = vmax + 1
    return flowratestorage

"This is used to vary psl whilst keeping density constant"

def slowingprobability(lanes,s,tmax,vmax,N,psl,psp,po):
    L = fillroad(lanes,s,N)
    flowratestorage = np.array([]) 
    densitystorage =  np.array([])
    while psl < 1:
        L = fillroad(lanes,s,N)
        totalflow = 0
        t = 0
        startcount(0)
        while t < tmax:
            flow = multitrafficovertaking(L,lanes,t,vmax,tmax,psl,psp,po,s)
            totalflow = totalflow + flow
          
            t = t + 1  
        flowrate = totalflow/(tmax-10*s) 
        flowratestorage = np.append(flowratestorage,flowrate)
        densitystorage =  np.append(densitystorage,psl)
        psl = psl + 0.1
    return flowratestorage,densitystorage   

"This function is identical to Traffic with an extra parameter to alter the initial transient time"

def Trafficinitialtransient(lanes,s,tmax,vmax,N,psl,psp,po,it):

    L = fillroad(lanes,s,N)
    
    flowratestorage = np.array([])  # These are empty arrays to store values for density and flowrate in
    densitystorage =  np.array([])
    
    while N < s/2:
        L = fillroad(lanes,s,N)
        totalflow = 0
        t = 0
        startcount(0)
        while t < tmax:
            flow = multitrafficovertakinginitialtransient(L,lanes,t,vmax,tmax,psl,psp,po,s,it)
            totalflow = totalflow + flow
              
            t = t + 1  
        
        flowrate = totalflow/(tmax-it*s)  
        density = N/s
        densitystorage = np.append(densitystorage,density)
        flowratestorage = np.append(flowratestorage,flowrate)
        N = N + 1    
    return flowratestorage,densitystorage  
        
"Time space plot function"
def multitimespaceplotting(L,r,t,vmax,tmax,psl,psp,po,s,lanes):   #This is acombination of all the functions
    v = carpositions(L,r)
    accelleration(v,L,r,vmax)
    braking(v,L,r,vmax)
    random(v,L,r,psl)
    overtakingl(v,L,r,po,lanes)
    overtakingr(v,L,r,po)
    timespaceplot(v,L,r,t,tmax,s)
    displacement(L,r,t,lanes)
    

