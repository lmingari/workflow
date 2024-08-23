#!/usr/bin/bash

module load anaconda3/2021.05
source activate lcapra

cd $path_post

python plot_deposit.py
python plot_colmass.py

convert -delay 20 -loop 0 colmass*.png animation.gif

