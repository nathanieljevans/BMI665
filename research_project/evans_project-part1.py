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
    # Find highest differntially expressed genes pathway 
    
    sorted_pathways = list(pathways.values())
    sorted_pathways.sort(reverse=True)
    
    ys = list(map(lambda x: x.odds_ratio, sorted_pathways))
    xs = list(range(len(ys)))
    
    plt.plot(xs, ys, '*', color='blue')
    plt.suptitle('sorted pathway odds ratio of DE genes')
    plt.ylabel('odds ratio')
    plt.xlabel('pathways')
    plt.plot(xs[0:5], ys[0:5], 'o', color='red')
    
    
    print('The pathway with the highest odds ratio for DE genes: \nName: %s\nID: %s' %(sorted_pathways[0].name, sorted_pathways[0].ID))
        
    with open('./outputs/chosen_pathway.pkl', 'wb') as f: 
        pickle.dump(sorted_pathways[0], f) 
        
    print(sorted_pathways[0].DE_genes)