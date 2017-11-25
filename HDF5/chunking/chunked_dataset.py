###  HDF5 CHUNKING DEMO
###------------------------------------------------------------------------------------------------ 
###
###  PART 1 - File Creation
###
###           In this section we will create a new HDF5 file with chunking enabled
###
###  Relevent information can be found at http://docs.h5py.org/en/latest/high/dataset.html#chunked-storage
###

import h5py
import numpy as np
import timeit, sys, contextlib

  # Set the array dimension we use for our datasets.  Each datset will be two dimensional 
  # (array_dim by array_dim)

array_dim = 4000
if len(sys.argv)>1:
   array_dim = int( sys.argv[1] )

  # Now, let's set a chunk dimension. Each chunk will be 2D (eg. chunk_dim by chunk_dim)

chunk_dim = 200
if len(sys.argv)>2:
   chunk_dim = int( sys.argv[2] )

  # Let's create a new HDF5 file.  Set its access attribute such that we will be able to write
  # data into it.

fid = h5py.File('chunkedfile.h5', 'w')

  # Create a array_dim x array_dim NumPy array of random floats. 

input_data = np.random.rand(array_dim,array_dim)

  # Construct an emtpy dataset with space enough to hold our matrix of floats. 

dset = fid.create_dataset( "ChunkedData", (array_dim,array_dim), dtype='f', chunks=(chunk_dim,chunk_dim) )

  # Notice the last option added to our dataset creation call.  The "chunks" flag tells
  # HDF5 that we want to employ a chunked storage patterm for this dataset.  The tuple
  # immediately following the "chunks" flag sets the set of each chunk. Remember the following:
  #  - # of chunk dimensions must equal # of dataset dimensions
  #  - chunk dimensions must evenly divide into the dataset's dimensions
  #
  # If you don't know what chunk dimensions to use, h5py can select them for you
  #
  #  dset = fid.create_dataset( "ChunkedData", (array_dim,array_dim), dtype='f', chunks=True )

  # Copy our 2D array of random floats into our new HDF5 dataset

dset[:,:] = input_data

  # Let's add some metadata that describes our new dataset to any user unfamiliar with the file.  
  # Create an attribute, calling it description and give a short line describing the data in
  # out new HDF5 dataset

dset.attrs["Description"] = "chunked 2D array of random floats"

print "\n Dimensionality and Chunking Check"
print "-----------------------------------"
print "  Chunked Dataset"
print "     overall dimensions : ", dset.shape
print "     chunk dimensions   : ", dset.chunks
print " "

  # Create a second dataset without chunking (i.e. using the default contiguous ordering). It
  # should contain the similarly sized matrix of floats used in the last two datasets.

dset2 = fid.create_dataset( "NonChunkedData", (array_dim,array_dim), dtype='f' )
dset2[:,:] = input_data
dset2.attrs["Description"] = "non-chunked 2D array of random floats"
print "  Non-compressed Dataset"
print "     overall dimensions : ", dset2.shape
print "     chunk dimensions   : ", dset2.chunks
print " "

###
###  PART 2 - Contiguous Read Performance 
###
###           In this section we will perform full contiguous reads of the datsets in their
###           entirety.  Performance should be similar as chunking will have no benefit when
###           performing contiguous I/O operations. 

  # Create an empty array_dim by array_dim matrix to hold the data to be read in

output = np.empty( (array_dim,array_dim), dtype='f' )

  # perform and time the two full-dataset contiguous reads
t = timeit.Timer( "output[:,:] = dset", "from __main__ import dset, output" )
time_chunked = t.timeit(1)

t = timeit.Timer( "output[:,:] = dset2", "from __main__ import dset2, output" )
time_nonchunked = t.timeit(1)

print "\n Contiguous Dataset Read Times"
print "-------------------------------"
print "  chunked     : %f sec" % (time_chunked,)
print "  non-chunked : %f sec\n" % (time_nonchunked,)

###
###  PART 3 - Non-contiguous Read Performance 
###
###           In this section we will perform non-contiguous reads.  We will again read the 
###           the entire contents of each dataset -but in columnwise fashion.  Since data is
###           stored row-wise be default in h5py, this will break the contiguous nature of 
###           the reads.

  # Create an empty vector of array_dim elements to hold the column data to be read in

output = np.empty( (array_dim,), dtype='f' )

  # perform and time the two full-dataset non-contiguous reads
s = """\
for n in range(array_dim):
    output[:] = dset[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset, output, array_dim" )
time_chunked = t.timeit(1)

s = """\
for n in range(array_dim):
    output[:] = dset2[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset2, output, array_dim" )
time_unchunked = t.timeit(1)

print "\n Non-contiguous Dataset Read Times"
print "-----------------------------------"
print "  chunked     : %f sec" % (time_chunked,)
print "  non-chunked : %f sec\n\n" % (time_unchunked,)

fid.close()

###
###  PART 4 - Read Performance and Chunk Cache size 
###
###           By default, the chunk cache is set to 1MB.  In this section, we try to improve
###           the observed non-contiguous read performance for the same compressed chunked
###           dataset used in Sections 1-3.

  # We need to employ the low-lvel HDF5 API to see the current File access properties. One of
  # properties will be chunk cache size

file_properties = h5py.h5p.create( h5py.h5p.FILE_ACCESS ) 
file_settings = list( file_properties.get_cache() )

print " Chunk cache sizes (bytes)"
print "---------------------------"
print " before modification : ", file_settings[2] 

  # Let's quadruple the chunk cache size to 4MB

file_settings[2] *= 4 
file_properties.set_cache( *file_settings )
print " after modification  : ", file_settings[2] 

  # Now, create a new HDF5 with the modified file access properties

filename = 'new_chunked_dataset.h5'
with contextlib.closing( h5py.h5f.create(filename, fapl=file_properties) ) as newFile:
     fid = h5py.File( newFile )

  # Create the same compressed and non-compressed datasets we used previously

dset = fid.create_dataset( "ChunkedData", (array_dim,array_dim), dtype='f', chunks=(chunk_dim,chunk_dim) )
dset2 = fid.create_dataset( "NonChunkedData", (array_dim,array_dim), dtype='f', data=input_data )

  # Fill both datasets with the same random data

input_data = np.random.rand(array_dim,array_dim)
dset[:,:] = input_data
dset2[:,:] = input_data

output = np.empty( (array_dim,), dtype='f' )

  # perform and time the two full-dataset non-contiguous reads

s = """\
for n in range(array_dim):
    output[:] = dset[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset, output, array_dim" )
time_chunked = t.timeit(1)

s = """\
for n in range(array_dim):
    output[:] = dset2[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset2, output, array_dim" )
time_unchunked = t.timeit(1)

print "\n\n Non-contiguous Dataset Read Times"
print "-----------------------------------"
print "  chunked     : %f sec" % (time_chunked,)
print "  non-chunked : %f sec\n" % (time_unchunked,)

fid.close()
