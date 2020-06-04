#!/usr/bin/env bash
#uniform no-fec
for i in $(seq 0.0001 0.0001 0.0004)
do
   python dfr_simulation.py -M uniform -P $i --no-fec --no-trace >> uniform_nofec.out
done

#uniform fec
for i in $(seq 0.0001 0.0001 0.0004)
do
   python dfr_simulation.py -M uniform -P $i --fec --no-trace >> uniform_fec.out
done

#sgm no-fec
for i in $(seq 0.0001 0.0001 0.0004)
do
   python dfr_simulation.py -M sgm -P $i --no-fec --no-trace >> sgm_nofec.out
done

#sgm fec
for i in $(seq 0.0001 0.0001 0.0004)
do
   python dfr_simulation.py -M sgm -P $i --fec --no-trace >> sgm_fec.out
done


#sgm no-fec
for i in $(seq 0.0001 0.09 0.9)
do
   python dfr_simulation.py -M sgm -P $i --no-fec --no-trace >> sgm_nofec_test.out
done