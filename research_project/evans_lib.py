# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:14:10 2018

@author: natha


odds ratio: https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%207/research_project_background_BMI565.pdf 

Project Description: https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%207/research_project_description_BMI565.pdf

kegg: https://www.genome.jp/kegg/pathway.html
https://www.genome.jp/dbget-bin/www_bget?pathway:map05222


The goal of this research project is to use differentially expressed genes following a flu infection to highlight critical infection response pathways. Next, we compare the conservation between species homologs for differentially expressed genes and non-differentially expressed genes to see how the conserved infection-response is between species. 
"""

data_path = './data/BMI565_ResearchProject_Data/'

import sys
from matplotlib import pyplot as plt 
import seaborn as sns 
from Bio import Entrez, AlignIO 
from Bio.Align.Applications import ClustalwCommandline
import os
import pickle 
import pandas as pd 
from scipy.stats import mannwhitneyu

class pathway: 
    '''
    This class represents a gene pathway, with various attributes and functions pertaining to the analysis of a specific pathway, primarily represented as a group of gene symbols. 
    '''
    def __init__(self, raw, DE, allPB): 
        '''
        parses pathway data and separates into differentially expressed genes and not.
        input
            raw <str> raw gene pathway data 
            DE <set> genes that are differentially expressed after flu infection 
            allPB <set> all genes included in the dataset 
            
        outputs 
            pathway object 
        
        '''
        Entrez.email = 'evansna@ohsu.edu' 
        
        self.ID, self.name, self.group = self.parse(raw)
        
        self.DE_genes = self.group.intersection(DE) # A
        self.nonDE_genes = self.group - self.DE_genes # B
        
        self.nonPathway_genes = allPB - self.group
        self.nonPathway_DE_genes = self.nonPathway_genes.intersection(DE) # C
        self.nonPathway_nonDE_genes = self.nonPathway_genes - self.nonPathway_DE_genes # D 

        self.odds_ratio = (len(self.DE_genes) * len(self.nonPathway_nonDE_genes)) / (len(self.nonDE_genes) * len(self.nonPathway_DE_genes))
    
    def parse(self, raw): 
        '''
        parses the raw pathway data 
        
        inputs 
            raw <str> data to be parsed
            
        outputs 
            ID <str> pathway ID 
            name <str> pathway name 
            group <set> pathway gene symbols <str> 
        '''
        s = raw.split('\t')
        ID = s[0]
        name = s[1]
        group = set(s[2:])
        
        return ID, name, group 
        
    def __eq__(self, other): 
        return (self.odds_ratio == other.odds_ratio) 
    
    def __lt__(self, other): 
        return (self.odds_ratio < other.odds_ratio)

    def get_gene_seq(self, gene_sym, species): 
        ''' 
        Retrieves the gene sequence from the nucleotide database (nuccore) and returns it as a fasta file in str format. 
        
        input
            gene_sym <str> gene_sym to search for 
            species <str> which species to return 
            
        output 
            fasta file <str> representing the search terms, <None> if the search fails. 
        '''
        assert species.lower() in set(['homo sapiens', 'mus musculus', 'canis lupus familiaris']), 'improper species input' 
        
        try: 
            # There are a number of failures, search results in no valid responses 
            search_handle = Entrez.esearch(db='nuccore',term= gene_sym + '[Gene] AND ' + species + '[porg]')
            record = Entrez.read(search_handle)
            ids = record["IdList"]
            #print('ids', ids)
            
            result = Entrez.efetch(db="nuccore", id=ids[0], rettype="fasta", retmode="xml")
            text = Entrez.read(result)[0]
            
            assert text['TSeq_orgname'].lower() == species.lower(), 'wrong species returned! Wanted: ' + species + ', received: ' + text['TSeq_orgname'] 
            
            return Entrez.efetch(db="nuccore", id=ids[0], rettype="fasta", retmode="txt").read()
        
        except: 
            print( "failed to retrieve the %s gene for %s species" %(gene_sym, species.upper()) ) 
            return None #entrez_search_failure
    
    def calculate_edit_distance(self, seq1, seq2): 
        
        count = 0 
        for b1, b2 in zip(seq1, seq2): 
            if (b1 == b2): 
                count += 1 
            
        return count / max( len(seq1), len(seq2) ) # normalize by length of gene: want the longer of the two 
        
        
    def get_edit_distances(self): 
        '''
        This funtion: 
            1. generates a fasta file for our 3 species of comparison 
            2. combines the 3 species sequences into a fasta file 
            3. writes that fasta file to disk 
            4. runs clustalw on the fasta file 
            5. reads alignment into ram 
            6. calculates edit distance
            
        
        '''
        Entrez.email = 'evansna@ohsu.edu'
        
        species = ['homo sapiens', 'mus musculus', 'canis lupus familiaris'] 
        
        fail = 0
        self.gene_edit_dist = {} 
        tot = len(self.group)
        
        for i,gene in enumerate(self.group): 
            ppprint(gene, fail, i, tot, 'entrez gene retrieval')
            #print('calculating edit distances for:', gene)
            
            # write fasta file to disk for comparison 
            human_fasta = self.get_gene_seq(gene, species[0])
            mouse_fasta = self.get_gene_seq(gene, species[1])
            dog_fasta = self.get_gene_seq(gene, species[2])
            fasta = [human_fasta, mouse_fasta, dog_fasta]
            
            if (None not in fasta): 
                ppprint(gene, fail, i, tot, 'clustalW align')
                full_fasta = '\n'.join(fasta)
    
                with open('./temp/unaligned.fasta', 'w') as f: 
                    f.write(full_fasta)
                    
                # run clustalw  
                clustalw_exe = '\\Program Files (x86)\\ClustalW2\\clustalw2.exe'
                target = 'aligned-' + gene + '.aln'
                output  = './temp/' + target
                if (target not in os.listdir('./temp/')): # Only do a realignment if necessary 
                    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
                    command = ClustalwCommandline(clustalw_exe, infile="./temp/unaligned.fasta", outfile = output)
                    stdout, stderr = command()
                    
                # read alignment file into ram 
                align = AlignIO.read(output, 'clustal')
                
                #print(align[0]) # mouse
                #print(align[1]) # dog
                #print(align[2]) # human
                
                # calculate edit distance # save human-mouse e-dist, human-canis e-dist 
                ppprint(gene, fail, i, tot, 'calc edit dist')
                self.gene_edit_dist[gene] = {'human-mouse' : self.calculate_edit_distance(align[2], align[0]), 'human-dog' : self.calculate_edit_distance(align[1], align[2])}
            
            else: 
                fail+=1 
                #print('failed to process: %s' % gene)
        
            with open('./data/edit_dists-test.pkl', 'wb') as f: 
                pickle.dump(self.gene_edit_dist, f)
         
        print('\nFinished calculating edit distances. Failures: %s' %fail)
            
            
    def plot_conservation(self, species, recalc = False, ax=None):
        '''
        This function creates a boxplot comparing conservation of differentially expressed genes vs non-differentially expressed genes within the pathway.
        
        input
            species <str> which homolog to compare, options are: human-mouse or human-dog
            
        output
            None 
        '''
        
        assert species in ['human-mouse','human-dog'], 'wrong species comparison input' 
        
        if (os.path.isfile('./data/edit_dists.pkl') and not recalc): 
            with open('./data/edit_dists.pkl', 'rb') as f: 
                self.gene_edit_dist = pickle.load(f)
                
        else: 
            self.get_edit_distances()
            
        DE_conserved = list(map(lambda x: self.gene_edit_dist[x][species], set(self.gene_edit_dist.keys()).intersection(self.DE_genes)))
        
        nonDE_conserved = list(map(lambda x: self.gene_edit_dist[x][species], set(self.gene_edit_dist.keys()).intersection(self.nonDE_genes)))
        
        cons = DE_conserved + nonDE_conserved
        dexp = ['DE']*len(DE_conserved) + ['non-DE']*len(nonDE_conserved)
        
        df = pd.DataFrame(data = {'conservation' : cons, 'DiffExp' : dexp } )
        
        
        sns.boxplot(x='DiffExp', y='conservation', data=df, ax=ax)
        
        ax.set_title(species)
        
        manwhit = mannwhitneyu(DE_conserved, nonDE_conserved)
        
        ax.text(x=-.2, y=-.03, s= 'Manwhitney P-Value: '+ str(manwhit.pvalue))
        
        print('Manwhitney test for species %s : %s' %(species.upper(), str(manwhit)))
    
class entrez_search_failure(Exception): 
    ''' 
    failure of search terms or connection
    ''' 
    
    def __str__(self): 
        return 'the entrez gene search failed to return a valid response' 

def ppprint(gene, fail, num, tot, msg): 
    '''
    prints a status msg to console over itself for cleaner presentation. 
    
    inputs 
        None
        
    Outputs 
        None 
    '''
    sys.stdout.write("Progress: %d/%d [failures: %d] \t Gene: %s   ...%s   \r" % (num, tot, fail, gene, msg) )
    sys.stdout.flush()
    
    