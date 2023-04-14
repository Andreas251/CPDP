sbatch --time=$1 --job-name=Transform_$2 --output=outputs/Transform_$2.o%j --error=errors/Transform_$2.e%j transform_slurm.sh $2 $3
