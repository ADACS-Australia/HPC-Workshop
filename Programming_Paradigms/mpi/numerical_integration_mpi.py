###  NUMERICAL INTEGRATION DEMO
###------------------------------------------------------------------------------------------------

## In this example we perform a very simple integration of an 1D function (f) over a
## given interval [x1,x2].  We use the simplisitic rectangular area approach to compute
## the area under the curve that f creates inside the specified interval.
##
## In this version, MPI parallelism is used

from mpi4py import MPI
import numpy as np

## Let's define the function that we integrate over the interval 

def integrate( x, dx ):
    area = 0.0
    for i in x:
        area += dx * (3.0 + i - 3.0*i*i)
    return area

## Now let's the interval over which we will integrate

x1 = 0.0
x2 = 1.0
    
## Define the width of each of the rectangles we use to determine the area.  Remember
## that the smaller the width, the more accurate our solution will be -but the time
## to solution will increase.

dx = 0.0000001 

## Determine the total number of rectangles of width dx are required to cover the
## interval of interest [x1,x2]

total_num_rectangles = int( (x2-x1)/dx )

## This leads to a number of rectangles per MPI task being

rectangles_per_MPI_task = int( total_num_rectangles / MPI.COMM_WORLD.Get_size() )

## Now, let's determine the global IDs of the first and last rectangles that each
## MPI task "owns" 

myID = MPI.COMM_WORLD.Get_rank()
start = rectangles_per_MPI_task * myID + 1
end = rectangles_per_MPI_task * (myID + 1) 

points = np.arange( start, end+1 )
points = points * dx

## Construct a loop where each MPI task computes the overall area for all rectangles
## it "owns".  Eg. the rectangles between start and end. 
## Remember that the area of a single rectange will be
## 
##      Area of a rectangle =  dx * f(x)
##
## where x is a point inside the [start,end] interval.

local_area = np.zeros(1)
local_area[0] = integrate( points, dx )

## Every MPI task then sends a copy of the 

computed_integral = np.zeros(1) 
MPI.COMM_WORLD.Reduce( local_area, computed_integral, op=MPI.SUM, root=0 )

if myID==0:    
   print "Computed integral of f was " + str(computed_integral[0]) 

## Let's compare our computed solution to the analytical solution

def g( x ):
    y = 3.0*x + 0.5*x*x - x*x*x;
    return y;

analytical_soln = g( x2 ) - g( x1 ) 
if myID==0:    
   print "Analytical solution was " + str(analytical_soln) 
