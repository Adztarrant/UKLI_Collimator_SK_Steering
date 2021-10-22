#!/bin/bash

source set_env.sh
rm log/* script/*
period_end=$(expr $(<"$1"))
period=$(expr $period_end - 7)
name="ukli"
#  for period in 304 306 336 340 358 371 383 386 388 389 411;
  while [ $period -le $period_end ];
  do
    sed -e 's/_per_/'$period'/g' process.sh > script/run_$period.sh
    chmod +x script/run_$period.sh
    echo "$name$period"
    qsub -r $name$period -e log/$period.e -o log/$period.o -q calib script/run_$period.sh
    ((period++))
  done

