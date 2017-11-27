#!/bin/bash
#SBATCH --job-name=integrate_serial
#SBATCH --output=Serial_Test.output
#SBATCH --partition=gpuq
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --account=courses01
#SBATCH --reservation=adacs
#SBATCH --export=NONE

##
## Load the necessary modules
##----------------------------

module load broadwell python numpy

##
## Change to the working directory
##---------------------------------

cd ${MYSCRATCH}

##
## Run the Python script
##-----------------------

srun --export=ALL -n 1 python ${HOME}/HPC-Workshop/Programming_Paradigms/serial/numerical_integration_serial.py 
