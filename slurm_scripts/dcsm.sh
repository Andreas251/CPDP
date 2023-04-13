#!/bin/bash -l

#SBATCH --job-name=Download_Dcsm  # Job name
#SBATCH --output=outputs/Download_Dcsm.o%j # Name of stdout output file
#SBATCH --error=errors/Download_Dcsm.e%j  # Name of stderr error file
#SBATCH --partition=small-g  # Partition (queue) name
#SBATCH --nodes=1              # Total number of nodes 
#SBATCH --ntasks-per-node=1     # 8 MPI ranks per node, 128 total (16x8)
#SBATCH --gpus-per-node=1       # Allocate one gpu per MPI rank
#SBATCH --time=1-12:00:00      # Run time (d-hh:mm:ss)         # Send email at begin and end of job
#SBATCH --account=project_465000374  # Project for billing

srun singularity exec --mount type=bind,src=/scratch/project_465000374,dst=/users/strmjesp/mnt nsrr.sif sh download_dcsm.sh
