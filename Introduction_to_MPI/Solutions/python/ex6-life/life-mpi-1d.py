#############################################################################
##  A simple implementation of John Conway's "Game of life" using MPI with an 
##  one-dimensional domain decomposition (NDIMS=1) in the x-direction.
##
##  The system is im x jm cells and runs for nsteps iterations.  Boundary 
##  conditions may be periodic or 'closed'.
#############################################################################

from mpi4py import MPI
import numpy as np

imtot = 16
jmtot = 16
nsteps = 12
periodic = 1

global_comm = MPI.COMM_WORLD
rank = global_comm.Get_rank()
size = global_comm.Get_size()

# Required MPI-related variables

req = [None, None]
my_tagl = 9999
my_tagr = 9998

# Check a regular 1-d decomposition is possible

if imtot % size != 0:
   print "Number of points not exactly divisible by number of MPI tasks"
   error_code = global_comm.Abort() 

# Create an one-dimensional Cartesian communicator. Set the local system size

ndims = 1
dims = MPI.Compute_dims( size, ndims )
comm = global_comm.Create_cart( dims, periods=(True,), reorder=True )

rank = comm.Get_rank()
my_left, my_right = comm.Shift( 0, 1 )
mycoords = comm.Get_coords( rank )

im = imtot / dims[0]
jm = jmtot
imp1 = im + 1
jmp1 = jm + 1
imp2 = im + 2
jmp2 = jm + 2

# Allocate a two-dimensional array for both old and new state
# Initialize both arrays to have all zero values

state_old = np.zeros( (imp2,jmp2), dtype=np.int ) 
state_new = np.zeros( (imp2,jmp2), dtype=np.int ) 

# Allocate the message buffers; for simplicity these are all of extent jmp2

sxl = np.zeros( (jmp2,), dtype=np.int )
sxr = np.zeros( (jmp2,), dtype=np.int )
rxl = np.zeros( (jmp2,), dtype=np.int )
rxr = np.zeros( (jmp2,), dtype=np.int )

# Initialize state, for example live cells marked 'X' ...
#
#         i=i0
#
# j-2     X
# j-1    X X
# j     XX XX

# Every rank must test to see if the relevant points are local...
# so the local x-coordinate for indexing the array should be offset by the 
# starting position in the global system.

i0 = imtot/2 - mycoords[0]*im
j  = jmtot/2

i = i0 - 2
if i >= 1 and i <= im:
    state_old[i][j] = 1

i = i0 - 1;
if i >= 1 and i <= im:
    state_old[i][j-1] = 1
    state_old[i][j  ] = 1 

i = i0
if i >= 1 and i <= im: 
   state_old[i][j-2] = 1

i = i0 + 1
if i >= 1 and i <= im:
    state_old[i][j-1] = 1
    state_old[i][j  ] = 1

i = i0 + 2
if i >= 1 and i <= im:
   state_old[i][j] = 1

# Allocate memory for the local and global live cell counters

lcount = np.empty( (1,), dtype=np.int )
ncount = np.empty( (1,), dtype=np.int )
    
# Time step loop (counting from 1...)

for n in range(nsteps):

  # Pack the x-direction buffers, exchange, and unpack
    sxl = state_old[1][:jmp2]
    sxr = state_old[im][:jmp2]

    req[0] = comm.irecv( source=my_right, tag=my_tagl )
    req[1] = comm.isend( sxl, dest=my_left, tag=my_tagl ) 
    req[1].wait()
    rxr = req[0].wait()

    req[0] = comm.irecv( source=my_left, tag=my_tagr )
    req[1] = comm.isend( sxr, dest=my_right, tag=my_tagr ) 
    req[1].wait()
    rxl = req[0].wait()

    state_old[0][1:jmp1] = rxl[1:jmp1]
    state_old[imp1][1:jmp1] = rxr[1:jmp1]

  # y-direction
    for i in range(imp2): 
        state_old[i][0]    = state_old[i][jm]
        state_old[i][jmp1] = state_old[i][1]

  # Count the number of living cells
    lcount[0] = (state_old[1:imp1][1:jmp1] == 1).sum()

  # Update the number of live cells
    for i in range(1,imp1):
        for j in range(1,jmp1):

            live = state_old[i-1:i+2][j-1:j+2].sum() - state_old[i][j]

            if (state_old[i][j]==1):
               if live == 2 or live == 3: # happy coexistence :)
                  state_new[i][j] = 1
               else:
                  state_new[i][j] = 0  # Starvation :(
            else:
               if (live == 3):
                  state_new[i][j] = 1  # Reproduction :))
               else:
                  state_new[i][j] = 0  # Still dead :((

  # Output
  #  print state_old[1:imp1][1:jmp1]
   
    ncount[0] = 0 
    comm.Reduce( lcount, ncount, op=MPI.SUM, root=0 ) 
    if rank==0:
       print "Step " + str(n) + " # of live cells : " + str(ncount[0]) 

  # Update time levels
    state_old = state_new
