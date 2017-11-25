#!/bin/bash
#SBATCH --job-name=integrate_mpi
#SBATCH --output=MPI_Test.output
#SBATCH --partition=gpuq
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --account=courses01
#SBATCH --reservation=adacs
#SBATCH --export=NONE

##
## Load the necessary modules
##----------------------------

module load broadwell mpi4py numpy gcc/5.4.0

# Set some necessary environment variables when using the MVAPICH library

export OMP_NUM_THREADS=0
export MV2_ENABLE_AFFINITY=0
export MV2_USE_THREAD_WARNING=0

##
## Change to the working directory
##---------------------------------

cd ${MYSCRATCH}

##
## Run the Python script
##-----------------------

srun --export=ALL -n 4 python ${HOME}/ADACS/programming_paradigms/mpi/numerical_integration_mpi.py 
