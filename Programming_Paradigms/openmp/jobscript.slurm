#!/bin/bash
#SBATCH --job-name=integrate_openmp
#SBATCH --output=OpenMP_Test.output
#SBATCH --partition=gpuq
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --account=courses01
#SBATCH --reservation=adacs
#SBATCH --export=NONE

##
## Load the necessary modules
##----------------------------

module load broadwell python gcc/5.4.0 numpy cython

##
## Run the Python script
##-----------------------

srun --export=ALL -n 1 python setup.py build_ext --inplace
srun --export=ALL -n 1 --cpu_bind=verbose,cores --export=all python numerical_integration_openmp.py
