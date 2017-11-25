#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=knlq
#SBATCH --time=00:10:00
#SBATCH --job-name=manycore-KNL
#SBATCH --output=manycore-KNL-%j.out
#SBATCH --reservation=adacs
#SBATCH --export=NONE

module load knl

srun -n 1 --export=all lscpu 
