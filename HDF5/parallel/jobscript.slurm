#!/bin/bash
#SBATCH --job-name=hdf5_parallel
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

module load broadwell python h5py-parallel 

export MV2_ENABLE_AFFINITY=0
export MV2_USE_THREAD_WARNING=0
export OMP_NUM_THREADS=0

##
## Change to the working directory
##---------------------------------

cd ${MYSCRATCH}

##
## Run the Python script
##-----------------------

srun --export=ALL -n 4 python ${HOME}/HPC-Workshop/HDF5/parallel/parallel_hdf5.py 
