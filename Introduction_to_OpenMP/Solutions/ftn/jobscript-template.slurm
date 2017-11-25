#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --reservation=adacs
#SBATCH --job-name=openmp-tutorial
#SBATCH --time=00:20:00
#SBATCH --export=NONE

module load broadwell gcc/5.4.0

export OMP_NUM_THREADS=4

echo "Hello World"
srun --export=all -n 1 ./hello-omp
echo "Pi-serial"
srun --export=all -n 1 ./pi-serial
echo "Pi-OpenMP version 1"
srun --export=all -n 1 ./pi-omp-v1
echo "Pi-OpenMP version 2"
srun --export=all -n 1 ./pi-omp-v2

