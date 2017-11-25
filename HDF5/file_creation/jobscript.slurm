#!/bin/bash
#SBATCH --job-name=hdf5_file_creation
#SBATCH --output=HDF5_Test
#SBATCH --partition=gpuq
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --account=courses01
#SBATCH --reservation=adacs
#SBATCH --export=NONE

##
## Load the necessary modules
##----------------------------

module load broadwell h5py numpy gcc/5.4.0 hdf5 

##
## Change to the working directory
##---------------------------------

cd ${MYSCRATCH}

##
## Run the Python script
##-----------------------

srun --export=ALL -n 1 python ${HOME}/ADACS/hdf5/file_creation/first_dataset.py
