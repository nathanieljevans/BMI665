# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 11:13:47 2018

@author: nathaniel evans
@class: BMI665: Scripting 
@HW: 2 
"""

import pickle

# wine file names to be processed 
wine_paths = ["white_wine_good.csv", "white_wine_poor.csv", "red_wine_good.csv", "red_wine_poor.csv"]

def find_avg_wines(file_names): 
    '''
    This function takes a list of file names which correspond to files stored in a directory named "data" in the same folder as this script. It then parses and processes the script to produce a dictionary such that: 
        top_dict(key = filename)
                -> inner_dict(key = data_metric_name)
                        -> average_value
    
    Args:
        file_names - list of strings
    Returns:
        fd - dict of dict
    '''
        
    fd = {}
    for fn in file_names: 
        with open("./data/" + fn, 'r') as f:
            nm = fn[0:-4]
            fd[nm] = {}
            header = f.readline().replace('\"', '').split(',')[0:-1]
            for head in header: 
                fd[nm][head] = 0
            
            n = 0
            for line in f.readlines(): 
                spl_line = line.strip('\n').split(',')
                for i, val in enumerate(spl_line): 
                    if (i<4):
                        fd[nm][header[i]] +=  float(val)
                n+=1
            for key in fd[nm]: 
                fd[nm][key] /= n
                    
    return fd
                    
# handles running in terminal and saving to pickled file in 'results' folder             
if __name__ == "__main__" :       
    avg_values = find_avg_wines(wine_paths)
    with open("./results/avg_wine_dict.pkl", 'wb') as fb: 
        pickle.dump(avg_values, fb)
    
