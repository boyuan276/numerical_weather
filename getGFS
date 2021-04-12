#!/bin/bash
echo "getting gfs data"
GFS_HOURS="00 06 12 18 24 30 36 42 48 54 60 66 72"
YEAR=$1
MONTH=$2
DAY=$3
RUNTIME=$4
url_tmplt="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."
file_tmplt="gfs.t12z.pgrb2.0p25.f0"
for i in $GFS_HOURS
do
echo wget $url_tmplt$YEAR$MONTH$DAY/$RUNTIME/atmos/${file_tmplt}$i
wget $url_tmplt$YEAR$MONTH$DAY/$RUNTIME/atmos/${file_tmplt}$i
done