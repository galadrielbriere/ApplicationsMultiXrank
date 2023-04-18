#!/bin/bash

#SBATCH --job-name=RWR
#SBATCH --mem=40GB
#SBATCH --account=ml_het_bio_nets
#SBATCH --cpus-per-task=20

module load python/3.9

python generate_rwr.py
