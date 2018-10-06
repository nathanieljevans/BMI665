## Created on Sat Oct  6 09:36:23 2018

## @author: nathaniel evans 
## @class: BMI665: Scripting 
## @HW: 1


#!/usr/bin/env bash 

mkdir -p download

wget -nc http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv -P ./download/ 

wget -nc http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv -P ./download/

mkdir -p data

sed 's/;/,/g' ./download/winequality-red.csv > ./data/wq-red.csv
sed 's/;/,/g' ./download/winequality-white.csv > ./data/wq-white.csv

# this can probably be done in one (or at least two) commands, instead of 4. Important if it were a large file. 
# Also, it'd be nice to keep the header line
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 > 5) print $3,$5,$9,$11,$12}' ./data/wq-red.csv > ./data/red_wine_good.csv 
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 < 5) print $3,$5,$9,$11,$12}' ./data/wq-red.csv > ./data/red_wine_poor.csv
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 > 5) print $3,$5,$9,$11,$12}' ./data/wq-white.csv > ./data/white_wine_good.csv
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 < 5) print $3,$5,$9,$11,$12}' ./data/wq-white.csv > ./data/white_wine_poor.csv

mkdir -p results 

python evans_analyze_wine.py
 