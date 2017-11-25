###  LUSTRE-NUMBER OF OSTS DEMO
###------------------------------------------------------------------------------------------------

## In this demo we will show how the size of stripes used to store a file in Lustre
## can effect the write and write performance from/to that file.

import os, shutil, sys

## Let's start by defining an array of stripe sizes.  Assume that the values are in megabytes.
## The values also do not have to be whole integers.

stripe_sizes = [0.125, 0.25, 0.5, 1, 2, 4]

## For each of the stripe sizes defined in our array, we will do the following:
##
##   - create a new directory named after the stripe size
##   - set the newly created directory to be striped over 4 OSTs and with a stripe set equal to
##     the array value
##   - generate a random test file in that directory and time how long it takes to write that
##     file in the new directory
##
## Here we go...

for stripe_size in stripe_sizes:

    print "\n------------------- NEW DIRECTORY -------------------\n\n "
    sys.stdout.flush()

  # create the new directory

    dirname = str(stripe_size) + "MB"
    command_str = "mkdir " + dirname 
    os.system( command_str ) 

  # set the new directory to be striped over 4 OSTs
 
    stripe_in_bytes = int(stripe_size * 1024 * 1024) 
    command_str = "lfs setstripe -c 4 -S " + str(stripe_in_bytes) + " " + dirname
    os.system( command_str )  

  # Notice that we use the command "lfs setstripe -S <number> directory" to set a particular
  # stripe size to a given directory.  When setting the stripe size, we must use a value
  # in terms of bytes -that's why we multiply our value arrays by 1024*1024 (since they are
  # in megabytes) 

  # Let's double-check that newly created directory has the expected Lustre stripe size

    command_str = "lfs getstripe -S -c " + dirname
    os.system( command_str )

  # We will use a tool called dd to generate a file filed with null characters (about 8.6GB worth).
  # Let's time how long it takes to generate this file in each of our striped directories. 

    test_file = os.getcwd() + "/" + dirname + "/test.dat" 
    command_str = "time dd if=/dev/zero of=" + test_file + " count=18k bs=1M"
    os.system( command_str )

  # We finish by deleting the test directory
    shutil.rmtree( dirname )
