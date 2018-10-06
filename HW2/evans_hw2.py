# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 11:13:47 2018

@author: nathaniel evans
@class: BMI665: Scripting 
@HW: 2 
"""

'''
Compare Low and High Quality
Now use Python code to determine what makes wine good or not. Create a Python function to read in
data from a given file path and calculate the average value of a given variable name.
# Example
avg_chloride_results = calculate_avg_value(data, "chlorides")
You want to automate as much as possible. So create a Python function that takes a list of the file names
and returns a dictionary.
The dictionary will have four keys equal to the given file names (e.g. the key for the file
white_wine_good.csv will be white_wine_good. The values of each filename key will be another
dictionary with keys being the four variables below and the values being the averages of each variable:
• Citric acid
• Chlorides
• pH
• Alcohol
# Example
wine_paths = ["white_wine_good.csv", ...]
avg_values = find_average_wines(wine_paths)
Save Results
Use the cPickle Python module to save the resulting dictionary to a file in a directory called results
(note: you’ll have to create this directory beforehand).
'''

wine_paths = ["white_wine_good.csv", "white_wine_poor.csv", "red_wine_good.csv", "red_wine_poor.csv"]

def make_dict(file_names): 
    
    fd = {}
    for fn in file_names: 
        with open("./data/" + fn, 'r') as f:
            nm = fn[0:-4]
            print(nm)
            fd[nm] = {"Citric acid":0,"Chlorides":0,"pH":0,"Alcohol":0}
            header = ["Citric acid","Chlorides","pH","Alcohol"]# If I fix awk to keep header row then include: #f.readline().split(',')
            
            n = 0
            for line in f.readlines(): 
                spl_line = line.strip('\n').split(',')
                print(spl_line)
                for i, val in enumerate(spl_line): 
                    if (i<4):
                        fd[nm][header[i]] +=  float(val)
                n+=1
            for key in fd[nm]: 
                fd[nm][key] /= n
                    
    print(fd)
                    
                
        
make_dict(wine_paths)
    
    
