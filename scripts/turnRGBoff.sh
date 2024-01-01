#!/bin/bash
# sudo i2cdetect -l 
mem=$(i2cdetect -l | grep 'SMBus I801 adapter at efa0'| cut -d$'\t' -f 1 | cut -d '-' -f 2)
/usr/sbin/i2cset -y $mem 0x27 0xe1 0x01
/usr/sbin/i2cset -y $mem 0x27 0xe2 0x01
/usr/sbin/i2cset -y $mem 0x27 0xe1 0x02
/usr/sbin/i2cset -y $mem 0x27 0xe1 0x03

