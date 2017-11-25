#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=courses01
#SBATCH --partition=gpuq
#SBATCH --reservation=adacs
#SBATCH --job-name=openmp-tutorial
#SBATCH --time=00:20:00
#SBATCH --export=NONE

module load broadwell gcc/5.4.0
module use /group/courses01/software/sles12sp2/modulefiles
module load mvapich forge
export LD_LIBRARY_PATH=/group/courses01/ADACS_workshop_2017/lib/gcc/5.4.0:$LD_LIBRARY_PATH

export DATA_DIR="/group/courses01/ADACS_workshop_2017/Datasets/matricies"

# The following example run is solving a 256x257 augmented matrix. 
# The DATA_DIR contains bigger matricies if you wish to experiment with them. 

# If profiling run the command line launching map. 
# Upon successful completion a *.map file will be generated which can be opened in Allinea MAP
map --profile --no-mpi ./gauss-serial -n 1024 -f $DATA_DIR/1024by1024.mat

# Otherwise for a normal run 
#srun --export=all -n 1 ./gauss-serial -n 256 -f $DATA_DIR/256by256.mat

