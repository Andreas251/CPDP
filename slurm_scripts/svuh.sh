#!/bin/bash -l

#SBATCH --job-name=Download_Svuh  # Job name
#SBATCH --output=outputs/Download_Svuh.o%j # Name of stdout output file
#SBATCH --error=errors/Download_Svuh.e%j  # Name of stderr error file
#SBATCH --partition=small-g  # Partition (queue) name
#SBATCH --nodes=1              # Total number of nodes 
#SBATCH --ntasks-per-node=1     # 8 MPI ranks per node, 128 total (16x8)
#SBATCH --gpus-per-node=1       # Allocate one gpu per MPI rank
#SBATCH --time=05:00:00      # Run time (d-hh:mm:ss)         # Send email at begin and end of job
#SBATCH --account=project_465000374  # Project for billing

#cat << EOF > select_gpu
#!/bin/bash

#export ROCR_VISIBLE_DEVICES=\$SLURM_LOCALID
#exec \$*
#EOF

#chmod +x ./select_gpu

#CPU_BIND="map_cpu:48"

#export MPICH_GPU_SUPPORT_ENABLED=1

#srun --cpu-bind=${CPU_BIND} singularity exec --mount type=bind,src=/scratch/project_465000374,dst=/users/strmjesp/mnt nsrr.sif sh download_sdo.sh 

srun singularity exec --mount type=bind,src=/scratch/project_465000374,dst=/users/strmjesp/mnt nsrr.sif sh download_svuh.sh

#srun --cpu-bind=${CPU_BIND} ./select_gpu <executable> <args>
#rm -rf ./select_gpu
