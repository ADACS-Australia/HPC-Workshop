###  LUSTRE-NUMBER OF OSTS DEMO
###------------------------------------------------------------------------------------------------

## In this demo we will show how the number of OSTs used to store a file in Lustre
## can effect the write and write performance from/to that file.

import os, shutil, sys, subprocess

## Let's start by defining an array of OST numbers.  Make sure you only use whole 
## integers.

num_osts = range(1,8) 

## For each number of OSTs, we will do the following:
##
##   - create a new directory named after the number of OSTs
##   - set the newly created directory to be striped over the specified number of OSTs 
##     with a stripe isize equal to 1MB
##   - generate a random test file in that directory and time how long it takes to write that
##     file in the new directory
##
## Here we go...

print "\n"
for N in num_osts:

  # create the new directory

    dirname = str(N) + "_OSTS"
    command_str = "mkdir " + dirname 
    os.system( command_str ) 

  # set the Lustre stripe size of the new directory to 1 MB. The number of OSTs it is striped 
  # over will be equal to N

    stripe_in_bytes = int(1024 * 1024) 
    command_str = "lfs setstripe -S " + str(stripe_in_bytes) + " -c " + str(N) + " " + dirname
    os.system( command_str )  

  # Let's double-check that newly created directory has the expected Lustre stripe size (using the -S flag)
  # and number of OSTs (using the -c flag)

    command_str = "lfs getstripe -S -c " + dirname
    os.system( command_str )

  # We will use a tool called dd to generate a file filed with null characters (about 8.6GB worth).
  # Let's time how long it takes to generate this file in each of our striped directories. 

    test_file = os.getcwd() + "/" + dirname + "/test.dat" 
    command_str = "time dd if=/dev/zero of=" + test_file + " count=18k bs=1M"
    os.system( command_str )

  # We finish by deleting the test directory

    shutil.rmtree( dirname )
