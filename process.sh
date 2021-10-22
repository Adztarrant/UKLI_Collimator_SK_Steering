#!/bin/bash

source set_env.sh

#period=0

#  while [ $period -le 203 ];
#  do
#    python runAsym.py --data $period $inj
    python runAsym.py --data _per_ 2
    python runAsym.py --data _per_ 3
    python runAsym.py --data _per_ 4
    python runAsym.py --data _per_ 5
    python runAsym.py --data _per_ 6
#    python runAsym.py --data $period 3
#    python runAsym.py --data $period 4
#    python runAsym.py --data $period 5
#    python runAsym.py --data $period 6
#    ((period++))
#    echo $period
#  done

#python runAsym.py --data 12 2
