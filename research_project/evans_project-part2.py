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
    genes2ID = {}  # list of genes (keys) -> sets of pathway IDs, Use this to search for all pathways that have X gene 
    for pw in raw_pathways[raw_pathways.index('\n'):].strip().split('\n'): 
        ID = pw[0:pw.index('\t')]
        pathways[ID] =  pathway(pw, DE, allPB) 
        for gene in pathways[ID].group : 
            if (gene in genes2ID): 
                genes2ID[gene].add(ID)
            else: 
                genes2ID[gene] = set([ID])
    
    # ------------------------------------------------------------------------
    # Find highest differnitally expressed genes pathway 
    #example = pathways[(list(pathways.keys()))[0]]
    #print( example.DE_genes ) 
    #print( example.nonDE_genes)
    #print( example.DE_genes.union( example.nonDE_genes ) == example.group)
    
    sorted_pathways = list(pathways.values())
    sorted_pathways.sort(reverse=True)
    #print(sorted_pathways[0])
    
    ys = list(map(lambda x: x.odds_ratio, sorted_pathways))
    xs = list(range(len(ys)))
    
    #plt.plot(xs, ys)
    
    tep = sorted_pathways[0] # top expression pathway (TEP)
    
    print('\n\n\n\n')
    print('ID:', tep.ID) 
    print('name:', tep.name)
    print('group:', tep.group)
    
    #print(tep.get_gene_seq(list(tep.group)[0], species = 'homo sapiens'))
    
    # species : Homo Sapiens, mus musculus, canis lupus
    
    
    #tep.get_edit_distances(list(tep.group)[0]) 
    
    #print(tep.gene_edit_dist)
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(11,9))
    plt.suptitle('Conservation of differentially expressed genes vs non-differentially expressed')

    tep.plot_conservation(species = 'human-mouse', recalc=False, ax=ax1)
    

    tep.plot_conservation(species = 'human-dog', recalc=False, ax=ax2)
    
