#!/bin/bash -l

#SBATCH --partition=small  # Partition (queue) name
#SBATCH --ntasks=1     # 8 MPI ranks per node, 128 total (16x8)
#SBATCH --cpus-per-task=5      # Allocate one gpu per MPI rank   # Send email at begin and end of job
#SBATCH --account=project_465000374  # Project for billing

srun singularity exec --mount type=bind,src=/scratch/project_465000374,dst=/users/strmjesp/mnt /scratch/project_465000374/train.sif python transform.py --dataset_name $1 --num_sub $2
