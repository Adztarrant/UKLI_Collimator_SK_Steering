#!/bin/bash

cat /home/pablofer/calib/analysis/sk_ukli/RION_BacteriaCounter/Supply_data/Supply_all.tsv /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202104* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202105* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202106* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202107* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202108* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202109* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202110* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202111* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202112* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_2022*> all_supply.tsv
#sed -i 's@/@-@g' all_supply.tsv
#sed -i 's/\t/ /g' all_supply.tsv
#sed -i '/Model/,+32d' all_supply.tsv
#sed -i '/FAIL/d' all_supply.tsv
python make_bacteria_graph.py all_supply.tsv
rm all_supply.tsv

cat /home/pablofer/calib/analysis/sk_ukli/RION_BacteriaCounter/Return_data/Return_all.tsv /home/water/public_html/RION_BacteriaCounter/Return/TSV/Return_202104* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202105* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202106* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202107* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202108* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202109* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202110* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202111* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_202112* /home/water/public_html/RION_BacteriaCounter/Supply/TSV/Supply_2022*> all_return.tsv
#sed -i 's@/@-@g' all_return.tsv
#sed -i 's/\t/ /g' all_return.tsv
#sed -i '/Model/,+32d' all_return.tsv
#sed -i '/FAIL/d' all_return.tsv
python make_bacteria_graph.py all_return.tsv
rm all_return.tsv

