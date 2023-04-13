#!/bin/bash -l

#SBATCH --partition=small  # Partition (queue) name
#SBATCH --ntasks=1              # Total number of nodes 
#SBATCH --cpus-per-task=10       # Allocate one gpu per MPI rank   # Send email at begin and end of job
#SBATCH --account=project_465000374  # Project for billing

srun singularity exec --mount type=bind,src=/scratch/project_465000374,dst=/users/strmjesp/mnt containers/nsrr.sif bash $1
