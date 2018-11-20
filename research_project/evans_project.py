# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:12:14 2018

@title: BMI665 Research Project 
@author: nathaniel evans 
@class: BMI665 

"""

data_path = './data/BMI565_ResearchProject_Data/'
from matplotlib import pyplot as plt 
import seaborn as sns 


class pathway: 
    
    def __init__(self, raw, DE, allPB): 
        self.ID, self.name, self.group = self.parse(raw)
        
        self.DE_genes = self.group.intersection(DE) # A
        self.nonDE_genes = self.group - self.DE_genes # B
        
        self.nonPathway_genes = allPB - self.group
        self.nonPathway_DE_genes = self.nonPathway_genes.intersection(DE) # C
        self.nonPathway_nonDE_genes = self.nonPathway_genes - self.nonPathway_DE_genes # D 
        
        self.odds_ratio = (len(self.DE_genes) * len(self.nonPathway_nonDE_genes)) / (len(self.nonDE_genes) * len(self.nonPathway_DE_genes))
    
    def parse(self, raw): 
        
        s = raw.split('\t')
        ID = s[0]
        name = s[1]
        group = set(s[2:])
        
        return ID, name, group 
        
    def __eq__(self, other): 
        return (self.odds_ratio == other.odds_ratio) 
    
    def __lt__(self, other): 
        return (self.odds_ratio < other.odds_ratio)

if __name__ == '__main__' : 
    
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
        
    pathways = {}   # gene ID -> pathway object 
    genes2ID = {}  # list of genes (keys) -> sets of pathway IDs
    for pw in raw_pathways[raw_pathways.index('\n'):].strip().split('\n'): 
        ID = pw[0:pw.index('\t')]
        pathways[ID] =  pathway(pw, DE, allPB) 
        for gene in pathways[ID].group : 
            if (gene in genes2ID): 
                genes2ID[gene].add(ID)
            else: 
                genes2ID[gene] = set([ID])
         
    #example = pathways[(list(pathways.keys()))[0]]
    #print( example.DE_genes ) 
    #print( example.nonDE_genes)
    #print( example.DE_genes.union( example.nonDE_genes ) == example.group)
    
    sorted_pathways = list(pathways.values())
    sorted_pathways.sort(reverse=True)
    print(sorted_pathways[0])
    
    
    ys = list(map(lambda x: x.odds_ratio, sorted_pathways))
    xs = list(range(len(ys)))
    
    plt.plot(xs, ys)
    
    tep = sorted_pathways[0] # top expression pathway (TEP)
    
    print('\n\n\n\n')
    print('ID:', tep.ID) 
    print('name:', tep.name)
    print('group:', tep.group)
    
    
    

    
    
