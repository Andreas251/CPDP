sbatch --time=$1 --job-name=split_$2 --output=outputs/split.o%j --error=errors/split.e%j ./SleepDataPipeline/slurm_scripts/split_slurm.sh $2 $3
