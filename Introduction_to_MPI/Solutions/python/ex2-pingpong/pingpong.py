##########################################################################
## 
##  An MPI program to send a message back and forth between two ranks
##  using a blocking send mpi_send(), and a blocking recieve mpi_recv().
##
##  NumPy is used to allocate the message buffer in terms of size and 
##  type.
##########################################################################


from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
   print "Must use exactly 2 MPI tasks"
   errorcode = comm.Abort()   

# Perform multiple exchanges between the 2 MPI Tasks
nexchange = 100
for i in range(nexchange):
    sender = i % 2
    recver = 1 - sender

    if rank==sender:
       data = np.ones( (1,), dtype=np.int )
       comm.Send( [data, MPI.INT], dest=recver, tag=9999 )
    else:
       data = np.empty( [1], dtype=np.int )
       comm.Recv( data, source=sender, tag=9999 )

