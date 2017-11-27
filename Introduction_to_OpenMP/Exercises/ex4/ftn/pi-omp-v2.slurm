#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --reservation=adacs
#SBATCH --job-name=openmp-exe1
#SBATCH --time=00:20:00
#SBATCH --export=NONE
module load broadwell gcc/5.4.0 
module use /group/courses01/software/sles12sp2/modulefiles
module load mvapich

export OMP_NUM_THREADS=4
srun --export=all -n 1 ./pi-omp-v1

