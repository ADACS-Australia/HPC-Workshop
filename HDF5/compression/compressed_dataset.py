###  HDF5 COMPRESSION DEMO
###------------------------------------------------------------------------------------------------
###
###  PART 1 - File Creation
###
###           In this section we will create a new HDF5 file with chunking and compression enabled.
###
###  Relevent information can be found at http://docs.h5py.org/en/latest/high/dataset.html#chunked-storage
###

import h5py
import numpy as np
import timeit, contextlib, sys

  # Set the array dimension we use for our datasets.  Each datset will be two dimensional
  # (array_dim by array_dim)

array_dim = 2500
if len(sys.argv)>1:
   array_dim = int( sys.argv[1] )
   if array_dim > 5000:
      array_dim = 5000

  # Now, let's set a chunk dimension. Each chunk will be 2D (eg. chunk_dim by chunk_dim)

chunk_dim = 250
if len(sys.argv)>2:
   chunk_dim = int( sys.argv[2] )
   if chunk_dim >= array_dim:
      chunk_dim = 250

  # Define a scale factor that we use to scale up the size of the chunk cache
chunk_cache_scale_factor = 4
if len(sys.argv)>3:
   chunk_cache_scale_factor = int( sys.argv[3] )

  # Let's create a new HDF5 file.  Set its access attribute such that we will be able to write 
  # data into it.

fid = h5py.File('compressedfile.h5', 'w')

  # Create a array_dim x array_dim NumPy array of random floats. 

input_data = np.random.rand(array_dim,array_dim)

  # Construct an emtpy dataset with space enough to hold our matrix of floats. Enable 
  # chunking and compression.

dset = fid.create_dataset( "CompressedData", (array_dim,array_dim), dtype='f', chunks=(chunk_dim,chunk_dim), compression="gzip" )

  # Notice the last option added to our dataset creation call.  The "compression" flag tells
  # HDF5 that we want to employ a particular compression filter to the data chunks.  In our example,
  # we are requesting Gzip compression of the chunks.  Other compression filters available include:
  #   -- lzf
  #   -- szip

  # Copy our 2D array of random floats into our new HDF5 dataset

dset[:,:] = input_data

  # Let's add some metadata that describes our new dataset to any user unfamiliar with the file.  
  # Create an attribute, calling it description and give a short line describing the data in
  # out new HDF5 dataset

dset.attrs["Description"] = "chunked 2D array of random floats GZipped compressed"

print "\n Dimensionality and Chunking Check"
print "-----------------------------------"
print "  Compressed + Chunked Dataset"
print "     overall dimensions : ", dset.shape
print "     chunk dimensions   : ", dset.chunks
print "     compression applied: ", dset.compression
print " "

  # Create a second dataset without compression but with chunking (i.e. using the default contiguous 
  # ordering).  It should also contain the similarly sized matrix of floats.

dset2 = fid.create_dataset( "ChunkedData", (array_dim,array_dim), dtype='f', chunks=(chunk_dim,chunk_dim) )
dset2[:,:] = input_data
dset2.attrs["Description"] = "chunked 2D array of random floats"
print "  Non-compressed + Chunked Dataset"
print "     overall dimensions : ", dset2.shape
print "     chunk dimensions   : ", dset2.chunks
print "     compression applied: ", dset2.compression
print " "

  # Create a third dataset without compression or chunking (i.e. using the default contiguous 
  # ordering).  It should contain the similarly sized matrix of floats used in the last two 
  # datasets.

dset3 = fid.create_dataset( "NonChunkedData", (array_dim,array_dim), dtype='f' )
dset3[:,:] = input_data
dset3.attrs["Description"] = "non-chunked 2D array of random floats"
print "  Non-compressed Dataset"
print "     overall dimensions : ", dset3.shape
print "     chunk dimensions   : ", dset3.chunks
print "     compression applied: ", dset3.compression
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
time_compressed = t.timeit(1)

t = timeit.Timer( "output[:,:] = dset2", "from __main__ import dset2, output" )
time_uncompressed = t.timeit(1)

t = timeit.Timer( "output[:,:] = dset3", "from __main__ import dset3, output" )
time_nonchunked = t.timeit(1)

print "\n Contiguous Dataset Read Times"
print "-------------------------------"
print "  compressed     : %f sec" % (time_compressed,)
print "  non-compressed : %f sec" % (time_uncompressed,)
print "  non-chunked    : %f sec\n" % (time_nonchunked,)

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
time_compressed = t.timeit(1)

s = """\
for n in range(array_dim):
    output[:] = dset2[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset2, output, array_dim" )
time_uncompressed = t.timeit(1)

s = """\
for n in range(array_dim):
    output[:] = dset3[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset3, output, array_dim" )
time_unchunked = t.timeit(1)

print "\n Non-contiguous Dataset Read Times"
print "-----------------------------------"
print "  compressed     : %f sec" % (time_compressed,)
print "  non-compressed : %f sec" % (time_uncompressed,)
print "  non-chunked    : %f sec\n\n" % (time_unchunked,)

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

  # Let's apply the cache cache scale factor we defined earlier to increase the size of the cache buffer

file_settings[2] *= chunk_cache_scale_factor 
file_properties.set_cache( *file_settings )
print " after modification  : ", file_settings[2] 

  # Now, create a new HDF5 with the modified file access properties

filename = 'new_compressed_dataset.h5'
with contextlib.closing( h5py.h5f.create(filename, fapl=file_properties) ) as newFile:
     fid = h5py.File( newFile )

  # Create the same compressed and non-compressed datasets we used previously

dset = fid.create_dataset( "CompressedData", (array_dim,array_dim), dtype='f', chunks=(chunk_dim,chunk_dim), compression="gzip" )
dset2 = fid.create_dataset( "NonCompressedData", (array_dim,array_dim), dtype='f', chunks=(chunk_dim,chunk_dim) )
dset3 = fid.create_dataset( "NonChunkedData", (array_dim,array_dim), dtype='f', data=input_data )

  # Fill both datasets with the same random data

input_data = np.random.rand(array_dim,array_dim)
dset[:,:] = input_data
dset2[:,:] = input_data
dset3[:,:] = input_data

output = np.empty( (array_dim,), dtype='f' )

  # perform and time the two full-dataset non-contiguous reads

s = """\
for n in range(array_dim):
    output[:] = dset[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset, output, array_dim" )
time_compressed = t.timeit(1)

s = """\
for n in range(array_dim):
    output[:] = dset2[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset2, output, array_dim" )
time_uncompressed = t.timeit(1)

s = """\
for n in range(array_dim):
    output[:] = dset3[:,n]
"""
t = timeit.Timer( s, "from __main__ import dset3, output, array_dim" )
time_unchunked = t.timeit(1)

print "\n\n Non-contiguous Dataset Read Times"
print "-----------------------------------"
print "  compressed     : %f sec" % (time_compressed,)
print "  non-compressed : %f sec" % (time_uncompressed,)
print "  non-chunked    : %f sec\n" % (time_unchunked,)

fid.close()
