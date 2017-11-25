#!/bin/bash
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --job-name=manycore-GPGPU
#SBATCH --output=manycore-GPGPU-%j.out
#SBATCH --reservation=adacs
#SBATCH --export=NONE

module load broadwell gcc/4.8.5 cuda 
export PATH=/group/courses01/ADACS_workshop_2017/bin:$PATH

srun -n 1 --export=all deviceQuery
