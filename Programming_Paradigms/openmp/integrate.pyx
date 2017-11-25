## We need to load a number of libraries and packages first

import cython
from cython.parallel import parallel, prange
from libc.stdlib cimport malloc, free

## We disable some of the checking to allow better performance (but we should be careful doing this!) 
@cython.boundscheck(False)
@cython.wraparound(False)
def integrate( double [:] x, double dx ):
  # we define some local variable using C types
    cdef int i, N
    cdef double integral_val = 0.0

  # Let's allocate a temporary array that holds the area values of all of the rectangles inside our
  # integration domain (eg. [x1,x2])
    N = x.shape[0]
    cdef double *areas = <double *>malloc( N*sizeof(double) )
    if not areas:
       raise MemoryError()

  # We spawn 4 OpenMP threads that compute the individual rectanglar areas in parallel.  Notice that
  # we no longer use a seperate f function anymore
#    try:
    with nogil, parallel(num_threads=4):
            for i in prange( N, schedule='static' ):
                areas[i] = dx * (3.0 + x[i] - 3.0*x[i]*x[i])
                
  # Finally, we sum up all the individual rectangular areas to get out final integral value. No 
  # locking or sychronization required as the addition is associative and ordering is not important.
            for i in prange( N, schedule='static' ):
                integral_val += areas[i]

    return integral_val
#    finally:
#       free(tmp)

