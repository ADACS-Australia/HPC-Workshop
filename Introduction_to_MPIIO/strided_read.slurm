#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --reservation=adacs
#SBATCH --job-name=adacs-mpi
#SBATCH --time=00:20:00
#SBATCH --export=NONE

export WORK_DIR=$MYSCRATCH/MPIIO
mkdir -p $WORK_DIR
cd $WORK_DIR
cp ~/HPC-Workshop/Introduction_to_MPIIO/strided_read .
module use /group/courses01/software/sles12sp2/modulefiles
module load broadwell gcc/5.4.0 
module load mvapich

srun -n 4 --export=all ./strided_read
