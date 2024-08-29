#!/bin/bash
#SBATCH --job-name=ps     # Job name
#SBATCH --mail-type=END,FAIL         # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --ntasks=30      
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-gpu=1
#SBATCH --mem-per-cpu=2000mb            
#SBATCH --partition=gpu
#SBATCH --distribution=cyclic:cyclic
##SBATCH --reservation=perez
#SBATCH --mem-per-cpu=2000mb          # Memory per processor
#SBATCH --time=7-00:00:00              # Time limit hrs:min:sec
#SBATCH --output=ps.log     # Standard output and error log

pwd; hostname; date
                   
source ~/.load_OpenMMv8_cuda12

for i in 1 2 3 4 5 6
do
if [ -e Logs/remd_000.log ]; then             #If there is a remd.log we are conitnuing a killed simulation
    prepare_restart --prepare-run  #so we need to prepare_restart
      fi
#launch_remd --platform CUDA --debug
srun --mpi=pmix_v3  launch_remd --debug
done


