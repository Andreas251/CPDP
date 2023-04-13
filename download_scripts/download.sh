sbatch --time=$1 --job-name=Download_$2 --output=outputs/Download_$2.o%j --error=errors/Download_$2.e%j download_slurm.sh $3
