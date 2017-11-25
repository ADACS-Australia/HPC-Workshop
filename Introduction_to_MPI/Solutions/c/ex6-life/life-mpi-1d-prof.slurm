#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --reservation=adacs
#SBATCH --job-name=adacs-mpi
#SBATCH --time=00:20:00
#SBATCH --export=NONE

module use /group/courses01/software/sles12sp2/modulefiles
module load broadwell gcc/5.4.0 
module load mvapich

export LD_LIBRARY_PATH=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0:$LD_LIBRARY_PATH
module load forge
map --profile -n 4 ./life-mpi-1d-prof
