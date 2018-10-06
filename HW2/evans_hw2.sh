## Created on Sat Oct  6 09:36:23 2018

## @author: nathaniel evans 
## @class: BMI665: Scripting 
## @HW: 1


#!/usr/bin/env bash 

## make download dir if not already present 
mkdir -p download

## download wine data if not already present 
wget -nc http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv -P ./download/ 
wget -nc http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv -P ./download/

## make data dir if not present
mkdir -p data

## replace all ; -> , and save to data folder as wq-red.csv and wq-white.csv
sed 's/;/,/g' ./download/winequality-red.csv > ./data/wq-red.csv
sed 's/;/,/g' ./download/winequality-white.csv > ./data/wq-white.csv


## filter data into 4 separate files based on wine quality value and including only specific metrics, keeping appropriate headers 
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 > 5) print $3,$5,$9,$11,$12}' ./data/wq-red.csv > ./data/red_wine_good.csv 
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 < 5) print $3,$5,$9,$11,$12}' ./data/wq-red.csv > ./data/red_wine_poor.csv
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 > 5) print $3,$5,$9,$11,$12}' ./data/wq-white.csv > ./data/white_wine_good.csv
awk 'BEGIN{FS=",";OFS=","} ; NR==1{print $3,$5,$9,$11,$12} ; NR>1{if ($12 < 5) print $3,$5,$9,$11,$12}' ./data/wq-white.csv > ./data/white_wine_poor.csv

## make results dir if not already present 
mkdir -p results 

## run python script to analyze filtered wine files and produce stat values
python evans_analyze_wine.py
 