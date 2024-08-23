#!/bin/sh

HOST='132.248.185.94'
USER='jose.solisag'
PASSWD='5GZrhS16'

cd /mnt/MD1200A/lcapra/cenizas/wrf-runs

ftp -v -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
bin
cd COLIMA
mget wrfout_*
quit
#
END_SCRIPT
mv wrfout* mexico.wrf.nc
exit 0
