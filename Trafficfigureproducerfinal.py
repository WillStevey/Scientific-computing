# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 12:51:43 2021
Traffic simulation investigation codes
@author: Wstev
"""
# Import all necessary modules
import numpy as np 
import matplotlib.pyplot as plt
import Trafficfunctionsmodule1 as Tf      # This contains all the basic functions used
import math

#%% Code to investigate the probability- not used in the lab report
pflow,p = Tf.slowingprobability(1,100,2000,5,10,0,0,0)
plt.plot(p,pflow)
plt.xlabel("Probabilty of slowing down")
plt.ylabel("flow")   
    

#%%Vmax investigation - repeat function 10 times and then we take the average used to produce figure 4 in the lab report
count = 0
vaverage = 0
while count < 10:
    vflow = Tf.Vmaxinvestigation(1,60,2000,0,6,0.5,0,0)
    vaverage = vaverage + vflow
    plt.plot(vflow,".")
    plt.xlabel("vmax")
    plt.ylabel("flow")
    count = count + 1

plt.plot(vaverage/count,label= "average")

#to run this code quickly change the while loop value from 10 to 1 so only one iteration of the code is run

#%% This code is ready to produce Figure 1 -averaged over 100 times
count = 0
plt.figure() 
averageflow = 0
plt.xlabel("Density")
plt.ylabel("Flow")
while count < 100:
    flow,density = Tf.Traffic(1,100,2000,5,0,0.5,0,0)
    plt.plot(density,flow,".")
    flow1 = flow
    averageflow = averageflow + flow1
    
    count = count + 1   
  
meanflow = averageflow/count   
plt.plot(density,meanflow,label='Average flow')  
plt.legend();  

#to run this code quickly change the while loop value from 100 to 1 so only one iteration of the code is run

#%% Convergence study code - keep density constant but vary L, density = 0.1 ,looking for the values to converge, furthermore we can vary the density and see how that alters convergence
densityconstant = 0.1
while densityconstant < 0.5:
    flow1 = np.array([])
    densitystorage = np.array([])
    s = 10
    N = math.ceil(s*densityconstant)
    while s < 100:
        N = math.ceil(s*densityconstant)
        flow,density = Tf.Traffic(1,s,2000,5,N,0.5,0,0)
        flow1 = np.append(flow1,flow[0])
        densitystorage = np.append(densitystorage,density[0])
       
        s = s + 1       
    Larrays = np.arange(10,100,1)  #the values of s used
    plt.plot(Larrays,flow1,label= np.round(densityconstant,4))
    plt.xlabel("Length of road")
    plt.ylabel("Flow")
    plt.legend(); 
    densityconstant = densityconstant + 0.05

#change density from 0.5 to 0.1 for code to run quickly ,it still takes several minutes to run though.
#%%initial transient study measure the flow rate at a constant density but only changing the cutoff.This would allow the code to be run for less timesteps with little difference
# This code is used to produce the graphs shown in figure 3
averageflow = 0
flow1 = np.array([])
densitystorage = np.array([])
Larrays = np.arange(1,11,1)
count = 0
while count < 5:
    
    flow1 = np.array([])
    it = 1
    s = 60
    N = 6
    while it < 11:
        Tmax = 2*s*it
        flow,density = Tf.Trafficinitialtransient(1,s,Tmax,5,N,0.5,0,0,it)
        flow1 = np.append(flow1,flow[0])
        densitystorage = np.append(densitystorage,density[0])
        
        it = it + 1       
    plt.plot(Larrays,flow1,".")
    averageflow = averageflow + flow1
    
    count = count + 1
 


plt.plot(Larrays,averageflow/count,label= "average")
plt.xlabel("Cutoff time (as a multiple of the road length")
plt.ylabel("Flow")
plt.legend(); 

#Change count from 5 to 1 to run the code quicker
#%% Compare the effects of overtaking compared to no overtaking - used to produce figure 6
count = 0
twolaneaverage = 0
twolaneaverageovertaking = 0
while count < 10:
    flow,density = Tf.Traffic(2,60,4000,5,0,0.5,0,0)
    plt.plot(density,flow,"bx")
    twolaneaverage = twolaneaverage + flow
    flow1,density1 = Tf.Traffic(2,60,4000,5,0,0.5,0,0.5)
    plt.plot(density1,flow1,"rx")
    twolaneaverageovertaking = twolaneaverageovertaking + flow1
    count = count + 1

plt.plot(density,twolaneaverage/count,label= "Without overtaking")
plt.plot(density1,twolaneaverageovertaking/count,label= "50% chance of overtaking")
plt.xlabel("Density")
plt.ylabel("Flow")
plt.legend(); 

#Change count from 10 to 1 to run the code quicker
#%% Compare the effects of different number of lanes  -used to produce figure 7
count = 0
onelaneaverage = 0
twolaneaverage = 0
threelaneaverage = 0
fourlaneaverage = 0
fivelaneaverage = 0
while count < 5:
    flow,density = Tf.Traffic(1,60,4000,5,0,0.5,0,0)
    plt.plot(density,flow,"bx")
    onelaneaverage = onelaneaverage + flow
    
    flow1,density1 = Tf.Traffic(2,60,4000,5,0,0.5,0,0.5)
    plt.plot(density1,flow1/2,"rx")
    twolaneaverage = twolaneaverage + flow1
    
    flow2,density2 = Tf.Traffic(3,60,4000,5,0,0.5,0,0.5)
    plt.plot(density2,flow2/3,"gx")
    threelaneaverage = threelaneaverage + flow2
    
    flow3,density3 = Tf.Traffic(4,60,4000,5,0,0.5,0,0.5)
    plt.plot(density3,flow3/4,"yx")
    fourlaneaverage = fourlaneaverage + flow3
    
    flow4,density4 = Tf.Traffic(5,60,4000,5,0,0.5,0,0.5)
    plt.plot(density4,flow4/5,"gx")
    fivelaneaverage = fivelaneaverage + flow4
    count = count + 1
    
plt.plot(density,onelaneaverage/count,label= "1 lane")
plt.plot(density1,twolaneaverage/(2*count),label= "2 lanes")   # The tra
plt.plot(density2,threelaneaverage/(3*count),label= "3 lanes")
plt.plot(density3,fourlaneaverage/(4*count),label= "4 lanes")
plt.plot(density4,fivelaneaverage/(5*count),label= "5 lanes")
plt.xlabel("Density")
plt.ylabel("Flow")
plt.legend(); 

#Again the count can be changed to 1 so only one iteration of the code is run
#%% Compare the effects of overtaking compared to no overtaking add speeding function
count = 0
twolaneaverage = 0
twolaneaverageovertaking = 0
while count < 1:
    flow,density = Tf.Traffic(2,60,4000,5,0,0.5,0,0)
    plt.plot(density,flow,"bx")
    twolaneaverage = twolaneaverage + flow
    flow1,density1 = Tf.Traffic(2,60,4000,5,0,0.5,0,0.5)
    plt.plot(density1,flow1,"rx")
    twolaneaverageovertaking = twolaneaverageovertaking + flow1
    count = count + 1

plt.plot(density,twolaneaverage/count,label= "No speeding")
plt.plot(density1,twolaneaverageovertaking/count,label= "50% chance of overtaking and speeding")
plt.xlabel("Density")
plt.ylabel("Flow")
plt.legend(); 

#%% Time space plotting used to produce figure 2
lanes = 1
s = 40
N = 4
t = 0
tmax = 800
Tf.startcount(0)
L = Tf.fillroad(lanes,s,N)
#L = Tf.fillroad(lanes,40,N)
while t < tmax:
    Tf.multitimespaceplotting(L,0,t,5,tmax,0.5,0,0,s,lanes)
    #Tf.multitimespaceplotting(L,0,t,5,800,0.5,0,0,40,lanes)
    t = t + 1
    
plt.xlabel("Position along the road") 
plt.ylabel("time")
plt.title("density =",N/s)
#run with s = 40 ,tmax = 800, for code to run faster, uncomment the lines of code in the above cell for this    
#%% From the convergence study  it was found you can run these
#codes and still get valid results for s = 40, which cuts down the time needed to run the codes



    
    
    
    
    
    
    

