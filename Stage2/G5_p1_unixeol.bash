#!/bin/bash
#######ZonadeParámetrosdesolicitudderecursosaSLURM################
#SBATCH --job-name=G5_p1_min_en
#SBATCH -p short
#SBATCH -N 1#Nodosrequeridos,Default=1
#SBATCH -n 10#Tasksparalelos,Default=1
#SBATCH --cpus-per-task=30
#SBATCH --mem=16384
#SBATCH --time=00:30:00
#SBATCH --mail-user=da.gomezp@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.log
##########################################################################
module load anaconda/python3.7
conda init
.~/.bashrc
conda activate G5_HW34_env
python p1.py