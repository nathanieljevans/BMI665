# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:12:14 2018

@title: BMI665 Research Project 
@author: nathaniel evans 
@class: BMI665 

"""
from evans_lib import *

from matplotlib import pyplot as plt 


if __name__ == '__main__' : 
    
    with open('./outputs/chosen_pathway.pkl', 'rb') as f: 
        tep = f.load(f)
    
    species = ( 'Homo Sapiens', 'mus musculus', 'canis lupus') 
    
    print('comparing gene conservation between: %s, %s and %s' %species)
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(11,9))
    plt.suptitle('Conservation of differentially expressed genes vs non-differentially expressed')
    
    tep.plot_conservation(species = 'human-mouse', recalc=False, ax=ax1)

    tep.plot_conservation(species = 'human-dog', recalc=False, ax=ax2)
    
    fig.savefig('./outputs/GeneConservationComparison.png')