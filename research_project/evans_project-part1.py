# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:12:14 2018

@title: BMI665 Research Project 
@author: nathaniel evans 
@class: BMI665 

"""
from evans_lib import *

from matplotlib import pyplot as plt 


data_path = './data/BMI565_ResearchProject_Data/'

if __name__ == '__main__' : 
    
    # data in ----------------------------------------------------------------
    raw_DE = ''
    with open(data_path + 'H5N1_VN1203_DE_Probes.txt') as f :
        raw_DE = f.read().strip()
        
    DE = set() # DE probes (gene symbol)
    for probe_DE in raw_DE.split('\n'): 
        DE.add(probe_DE.split('\t')[1]) # just take gene symbol
        
    raw_probes = '' 
    with open(data_path + 'H5N1_VN1203_UNIVERSE_Probes.txt') as f : 
        raw_probes = f.read().strip()
        
    allPB = set() # all probes (gene symbol)
    for probe in raw_probes.split('\n'): 
        allPB.add(probe.split('\t')[1]) # just take gene symbol    
    
    raw_pathways = ''
    with open(data_path + 'KEGG_Pathway_Genes.txt') as f : 
        raw_pathways = f.read().strip()
    # ------------------------------------------------------------------------
    # parse data and create pathway objects 
    pathways = {}   # gene ID -> pathway object 
    for pw in raw_pathways[raw_pathways.index('\n'):].strip().split('\n'): 
        ID = pw[0:pw.index('\t')]
        pathways[ID] = pathway(pw, DE, allPB) 
    
    # ------------------------------------------------------------------------
    # Find highest differnitally expressed genes pathway 
    #example = pathways[(list(pathways.keys()))[0]]
    #print( example.DE_genes ) 
    #print( example.nonDE_genes)
    #print( example.DE_genes.union( example.nonDE_genes ) == example.group)
    
    sorted_pathways = list(pathways.values())
    sorted_pathways.sort(reverse=True)
    
    ys = list(map(lambda x: x.odds_ratio, sorted_pathways))
    xs = list(range(len(ys)))
    
    plt.plot(xs, ys, '*', color='blue')
    plt.suptitle('sorted pathway odds ratio of DE genes')
    plt.ylabel('odds ratio')
    plt.xlabel('pathways')
    plt.plot(xs[0:5], ys[0:5], 'o', color='red')
    
    for i in range(5):
        print(sorted_pathways[i].name)
        
    with open(./data/)