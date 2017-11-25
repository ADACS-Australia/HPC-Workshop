#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --reservation=adacs
#SBATCH --job-name=openmp-exe1
#SBATCH --time=00:20:00
#SBATCH --export=NONE

module use /group/courses01/software/sles12sp2/modulefiles
module load broadwell gcc/5.4.0 
module load mvapich

srun -n 4 --export=all ./hello-mpi
