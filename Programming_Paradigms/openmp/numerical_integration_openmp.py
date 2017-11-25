## In this example we perform a very simple integration of an 1D function (f) over a
## given interval [x1,x2].  We use the simplisitic rectangular area approach to compute
## the area under the curve that f creates inside the specified interval.
##
## In this version,  we employ OpenMP to introduce some domain decomposition.  I.e. we
## allocate some rectangles to every OpenMP thread to create the overall global area
## value (which serves as an estimate of the integral of our target function). 

import numpy as np
import integrate

## Now let's the interval over which we will integrate

x1 = 0.0
x2 = 1.0
    
## Define the width of each of the rectangles we use to determine the area.  Remember
## that the smaller the width, the more accurate our solution will be -but the time
## to solution will increase.

dx = 0.0000001
points = np.arange( x1+dx, x2+dx, dx )

computed_soln = integrate.integrate( points, dx )

print "Computed integral of f was " + str(computed_soln) 

## Let's compare our computed solution to the analytical solution

def g( x ):
    y = 3.0*x + 0.5*x*x - x*x*x;
    return y;

analytical_soln = g( x2 ) - g( x1 ) 
print "Analytical solution was " + str(analytical_soln) 
