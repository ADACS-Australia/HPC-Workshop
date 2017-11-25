#!/bin/bash
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --time=00:10:00
#SBATCH --job-name=multicore_arch
#SBATCH --output=multicore_arch-%j.out
#SBATCH --reservation=adacs
#SBATCH --export=NONE

module load broadwell 

srun -n 1 --export=all lscpu
