#!/bin/csh
#PBS -N %NAME%_wrf
#PBS -A %PROJECTCODE%
#PBS -l walltime=8:30:00
#PBS -q regular
#PBS -j oe
#PBS -m abe
#PBS -M bnb.chey.mon@gmail.com
#PBS -l select=8:ncpus=32:mpiprocs=32
limit stacksize unlimited
cd %DIRECTORY%
###mpiexec_mpt -n 64 ./wrf.exe
###mpiexec_mpt dplace -s 1 ./wrf.exe
mpiexec_mpt ./wrf.exe
%OUTPUT%
exit