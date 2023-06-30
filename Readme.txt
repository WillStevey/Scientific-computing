Scientific computing - William Stevenson - Traffic project Read me

Numpy,Matplotlib.pyplot and Math were all imported and used in the code provided

This code consists of 4 python files:
Trafficfunctionsmodule1.py
Trafficfigureproducer.py
Trafficanimationsmodule
Trafficfunctionsmodule1.py

Trafficfunctionsmodule1.py contains all the functions needed to implement each step of the algorithm 
Trafficfigureproducer.py calls these functions in various combinations for each investigation
Trafficanimationsmodule - used for plotting and animating traffic flow
Trafficfunctionsmodule.py - called by the traffic animations module

The basic principles of the code are to have an array(L) that contains the positions of the cars and their velocities,their positions are stored as
there index along the array and there velocities are the value af the array element. Empty spaces on the road are represented by none values.

Each step of the algorithm is split into its own function
-The carpositions function finds the position of the cars by looping through L and finding the indexes of all the cars
-The acceleration function any car which is not at maximum speed will accellerate by one
-Braking function if there are any nearby cars a car will slow down 
-Random function each car has a random chance of slowing down by 1
-Displacement function, this will displace each car by its velocity ,if a car would go past the length of the road it will be sent back 
to the start and it will be counted to find out the flow of cars. 

These are the basic steps used to replicate the results from the reference paper 

Additional features have been added as functions

-Multiple lanes can be plotted allwoing larger roads to be simulated
- Overtaking has been implemented allowing drivers that are stationary on one road a chance to swap lanes if there is an empty space
- Speeding -there is a chance drivers can exceed the maximum speed limit 
- timespaceplotting - a plot of the positions of the cars as a function of time can be produced 
- animations

-variations of the main code that allow the cutoff point for initial transients to be varied
- A traffic function has been implemented which allows all 7 parameters to be entered and an array of flowrates with their corresponding densities will be found
- The code is completely modular allowing the investigations to be eaily conducted using a combination of the functions in Trafficfunctionsmodule1.py and some simple while loops

Limitations of the code
- The code does not scale well with increasing lengths of the road, as to find the positions of the cars every timestep a while loop is used over the length of the road
,this is only used once every timestep as the postions of the cars only need to be found once per timestep. The other while loops in the code are not a huge issue as they 
are only looping over the Number of cars which is relatively low compared to the length of the road.
- For a similar reason running the code for multiple lanes also slows down the code quite a bit.
- The random elements of speeding up and slowing down are completely random a better simulation would have driver charecteristics factor in as part of the simulation.

Future improvements
- Speed the code up by not considering the arrays,instead only consider the initial positions of the cars, use the code to find the new postions of the cars and save them to an array
that contains the new car positions this would cutting out the while loop that needs to be called each timestep.
- Create a seperate array that keeps track of each car,this would allow different driver charecteristics to be modelled eg reckless drivers who have a high chance of speeding.

The main function used in the code is the Traffic function which combines all the features into one code
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

How to run the report code:
-Save both Trafficfunctionsmodule1.py and Trafficfigureproducer.py into the same directory
-Run Trafficfunctionsmodule1.py first as it is imported into Trafficfigureproducer.py
-Run each cell of Trafficfigureproducer.py to produce the figures seen in the report,for the report mnay of the functions are looped and the
average is taken to reduce the error from the random parts of the code.So these codes all take some time to run, i reccomend you change the number
of iterations to one for each code, a folder of test figures to make sure you get similar results will be supplied in the zip file.
-Any of the general parameters can also be changed,to run the code really quicky set s = 40,and Tmax = 800 as this is the bare minimum needed to get decent results
see convergence studies for minimum value of L.

Report code run times
-all codes take 1-5 minutes for just one iteration ,change loops from 10 to 1 to make sure code runs quickly
How run the animation code:
-Save both Trafficfunctionsmodule.py and Trafficanimationsmodule.py from the animation folder into the same but seperate directory then the report code
-Run Trafficfunctionsmodule.py first as it is imported into Trafficanimationsmodule.py
- Run Trafficanimationsmodule.py to create an animation that shows multiple lanes and overtaking.
