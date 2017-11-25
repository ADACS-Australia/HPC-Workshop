###  PARALLEL HDF5 DEMO
###------------------------------------------------------------------------------------------------
###  How to run this script:
###
###         module load broadwell python h5py-parallel
###         salloc --partition workq --time 00:15:00 --ntasks 4
###         export MV2_ENABLE_AFFINITY=0
###         export MV2_USE_THREAD_WARNING=0
###         export OMP_NUM_THREADS=0
###         srun -n 4 python parallel_hdf5.py <array_dimension> 
###
###         *please note that <array_dimension> is optional
###
###------------------------------------------------------------------------------------------------
###
###  PART 1 - File Creation
###
###           In this section we will create a new HDF5 file with a dataset and attributes.

  # Import the h5py, NumPy and mpi4py packages

import h5py
import numpy as np
from mpi4py import MPI
import sys

# MPI Task 0 will initially set the test array dimension (using a set value or command-line input
# from the user). It will then broadcast the value to all other active MPI tasks.
 
mpi_rank = MPI.COMM_WORLD.rank

array_dim = np.empty( 1, dtype=int)
if mpi_rank==0:
   array_dim[0] = 10000
   if len(sys.argv)>1:
      array_dim[0] = int( sys.argv[1] )

MPI.COMM_WORLD.Bcast( array_dim, root=0 )

# We create a MPI Info object that sets propertoes such as the caching characteristics for the
# underlying Lustre filesystem. We also set the striping parameters (block size, # of OSTs).

mpi_info = MPI.Info.Create()
mpi_info.Set( "romio_ds_write", "disable" )
mpi_info.Set( "romio_cb_write", "automatic" )
mpi_info.Set( "striping_unit", "2097152" )  # size of a Lustre stripe in bytes
mpi_info.Set( "striping_factor", "2" ) # number of OSTs

  # Let's create a new HDF5 file called myfile.h5.  Set its access attribute such that we
  # will be able to write data into it.

fid = h5py.File('my_parallel_file.h5', 'w', driver='mpio', comm=MPI.COMM_WORLD, info=mpi_info )

  # The final two arguments configure the new HDF5 for parallel access via MPI-I/O.  The last
  # argument denotes the MPI communicator.  The default setting is MPI.COMM_WORLD and this will
  # work for most situations.

###
### PART 2 - Dataset Creation

  # Our dataset will be a 2D matrix.  Initially, we assume the each MPI task contains 1 row
  # of the 2D matrix.  We define the length of each row held by a MPI task as N. If we have P
  # MPI tasks, out dataset will be a 2D matrix of dimensions [ P by N ].

  # Let's create an integer array of length array_dim.  Each MPI task then sets every element of 
  # that array to its MPI Task ID 

row = np.empty( array_dim[0] )

row.fill( mpi_rank )

  # Let's define the dataset in our new HDF5 file. We start by constructing an emtpy dataset with  
  # enough space to hold our input_data array.

dset = fid.create_dataset( "MPIRankMatrix", (MPI.COMM_WORLD.size,array_dim[0]), dtype='i' )

  # Remember that every MPI task only has 1 row of the entire (global) dataset.  Thus we must 
  # allocate enough space to hold N integers for every MPI Task.

  # Each MPI task now writes its row into our new HDF5 dataset

dset[mpi_rank,:] = row


###
### PART 3 - Attribute Creation

  # Let's add some metadata that describes our new dataset to any user unfamiliar with the file.  
  # Create an attribute, calling it description and give a short line describing the data in
  # out new HDF5 dataset

dset.attrs["Description"] = "an 1D array of random floats"

  # Let's check if all of our input_data array was actually copied to the new dataset

if mpi_rank==0:
   print "dataset dimensions are ", dset.shape
   print "dataset datatype is ", dset.dtype
   print "chunk dimensions are ", dset.chunks


###
### PART 4 - Dataset Read

  # Let's read the row information back. Each MPI task only reads in its relevent row 

MPI.COMM_WORLD.Barrier()

row = np.empty( array_dim[0] )
row[:] = dset[mpi_rank,:]
print row[1:10]

  # Remember to close the file before ending your program.  This ensures that any 
  # pending writes or modifications are completed.

fid.close()
