#!/bin/tcsh
#PBS -N boyuan_wrf
#PBS -A UCOR0051
#PBS -l walltime=8:30:00
#PBS -q regular
#PBS -j oe
#PBS -m abe
#PBS -M by276@cornell.edu
#PBS -l select=2:ncpus=8:mpiprocs=8
limit stacksize unlimited
###mpiexec_mpt -n 64 ./wrf.exe
###mpiexec_mpt dplace -s 1 ./wrf.exe
mpiexec_mpt ./wrf.exe
%OUTPUT%
exit
