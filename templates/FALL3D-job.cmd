#!/bin/bash

#$ -q all.q
#$ -S /bin/bash
#$ -N FALL3D
#$ -o $path_run/job.out
#$ -e $path_run/job.err
#$ -pe openmpi $NMPI

. /etc/profile.d/modules.sh

module load fall3d/gcc/8.3

RUNDIR=$path_run
INPFILE="$project.inp"
TASK="all"
NX=$NMPIX
NY=$NMPIY
NZ=$NMPIZ
NENS=1
NP=$((NX*NY*NZ*NENS))

cd $RUNDIR
mpirun -np ${NP} Fall3d.r8.x ${TASK} ${INPFILE} ${NX} ${NY} ${NZ} -nens ${NENS}
