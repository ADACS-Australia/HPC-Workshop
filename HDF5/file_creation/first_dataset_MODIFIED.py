###  HDF5 FILE CREATION DEMO
###------------------------------------------------------------------------------------------------
###  How to run this script:
###
###         module load broadwell h5py numpy gcc/5.4.0 hdf5
###         salloc --partition workq --time 00:15:00 --ntasks 1
###         srun -n 1 python first_dataset.py
###
###  Relevent information can be found at: http://docs.h5py.org/en/latest/high/dataset.html
###
###------------------------------------------------------------------------------------------------ 
###  PART 1 - File Creation
###
###           In this section we will create a new HDF5 file with a dataset and attributes.

  # Import the h5py and NumPy packages

import h5py
import numpy as np

  # Set the array length we use for our dataset.

array_len = 1500

  # Let's create a new HDF5 file called myfile.h5.  Set its access attribute such that we
  # will be able to write data into it.

fid = h5py.File('myfile.h5', 'w')


###
### PART 2 - Dataset Creation

  # Let's add our first dataset: an 1D array consisting of array_len random floats.
  # Start by creating a NumPy array of random floats. 

input_data = np.random.rand(array_len)

  # Let's define a dataset. We start by constructing an emtpy dataset with space enough 
  # to hold our input_data array.

dset = fid.create_dataset( "RandomData", (array_len,), dtype='f' )

  # Copy our array of random floats into our new HDF5 dataset

dset[:] = input_data

  # NOTE: We could have replaced the 2 commands above with a single line:
  #
  # dset = fid.create_dataset( "RandomData", data=input_data )
  #


###
### PART 2a - Second Dataset Creation

input_data = np.random.random_integers( 4, size=array_len)
int_dset = fid.create_dataset( "RandomIntegerData", (array_len,), dtype='i' )
int_dset[:] = input_data


###
### PART 3 - Attribute Creation

  # Let's add some metadata that describes our new dataset to any user unfamiliar with the file.  
  # Create an attribute, calling it description and give a short line describing the data in
  # out new HDF5 dataset

dset.attrs["Description"] = "an 1D array of random floats"

  # Let's check if all of our input_data array was actually copied to the new dataset

print "Length of our dataset is ", dset.shape[0]
print "Datatype of our dataset is ", dset.dtype

  # Let's check if the description attribute was successfully created. If it was, output the 
  # description string we entered

if 'Description' in dset.attrs:
   print "dataset is described as ", dset.attrs['Description']

  # Notice that we access attribute values in a dictionary fashion.


###
### PART 3a - Adding the "units" attribute to both datasets

dset.attrs["Units"] = "killer hodgehogs"
int_dset.attrs["Units"] = "fuzzy rabbits"


###
### PART 4 - Dataset Read

  # Read the contents of our dataset into another NumPy array and display the results

output = np.empty( array_len, dtype='f' )
output[:] = dset
print output

  # Remember to close the file before ending your program.  This ensures that any 
  # pending writes or modifications are completed.

fid.close()
