###  NUMERICAL INTEGRATION DEMO
###------------------------------------------------------------------------------------------------

## In this example we perform a very simple integration of an 1D function (f) over a
## given interval [x1,x2].  We use the simplisitic rectangular area approach to compute
## the area under the curve that f creates inside the specified interval.
##
##  In this version, no parallelism is present.

import numpy as np

## Let's define the function that we integrate over the interval 

def f( x ):
    y = 3.0 + x - 3.0*x*x
    return y

## Now let's the interval over which we will integrate

x1 = 0.0
x2 = 1.0
    
## Define the width of each of the rectangles we use to determine the area.  Remember
## that the smaller the width, the more accurate our solution will be -but the time
## to solution will increase.

dx = 0.0000001 
points = np.arange( x1+dx, x2+dx, dx )

## Construct a loop where we start at x1 and progressively add rectangules of
## a width of dx until we reach x2.  Remember that the area of a single rectange will
## be 
##      Area of a rectangle =  dx * f(x)
##
## where x is a point inside the [x1,x2] interval.

area = 0.0
for x in points:
    area += dx * f( x )
    
print "Computed integral of f was " + str(area) 

## Let's compare our computed solution to the analytical solution

def g( x ):
    y = 3.0*x + 0.5*x*x - x*x*x;
    return y;

analytical_soln = g( x2 ) - g( x1 ) 
print "Analytical solution was " + str(analytical_soln) 
