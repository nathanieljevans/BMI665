# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:12:14 2018

@title: BMI665 Research Project 
@author: nathaniel evans 
@class: BMI665 

odds ratio: https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%207/research_project_background_BMI565.pdf 

Project Description: https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%207/research_project_description_BMI565.pdf

kegg: https://www.genome.jp/kegg/pathway.html
https://www.genome.jp/dbget-bin/www_bget?pathway:map05222


The goal of this research project is to use differentially expressed genes following a flu infection to highlight critical infection response pathways. Next, we compare the conservation between species homologs for differentially expressed genes and non-differentially expressed genes to see how the conserved infection-response is between species. 
"""

data_path = './data/BMI565_ResearchProject_Data/'


from matplotlib import pyplot as plt 
import seaborn as sns 
from Bio import Entrez, AlignIO 
from Bio.Align.Applications import ClustalwCommandline
import os
import pickle 
import pandas as pd 
from scipy.stats import mannwhitneyu


class pathway: 
    
    def __init__(self, raw, DE, allPB): 
        Entrez.email = 'evansna@ohsu.edu' 
        
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

    def get_gene_seq(self, gene_sym, species): 
        # returns fasta file text 
        
        
        assert species.lower() in set(['homo sapiens', 'mus musculus', 'canis lupus familiaris']), 'improper species input' 
        
        try: 
            
            search_handle = Entrez.esearch(db='nuccore',term= gene_sym + '[Gene Name] AND ' + species + '[organism]')
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
            
        return count / min( len(seq1), len(seq2) )
        
        
    def get_edit_distances(self, gene): 
        '''
        This funtion: 
            1. generates a fasta file for our 3 species of comparison 
            2. combines the 3 
        
        '''
        
        species = ['homo sapiens', 'mus musculus', 'canis lupus familiaris'] 
        
        self.gene_edit_dist = {} 
        
        for gene in self.group: 
            print('calculating edit distances for:', gene)
            
            # write fasta file to disk for comparison 
            human_fasta = self.get_gene_seq(gene, species[0])
            mouse_fasta = self.get_gene_seq(gene, species[1])
            dog_fasta = self.get_gene_seq(gene, species[2])
            fasta = [human_fasta, mouse_fasta, dog_fasta]
            
            if (None not in fasta): 
            
                full_fasta = '\n'.join(fasta)
    
                with open('./temp/unaligned.fasta', 'w') as f: 
                    f.write(full_fasta)
                    
                # run clustalw  
                clustalw_exe = '\\Program Files (x86)\\ClustalW2\\clustalw2.exe'
                output  = './temp/aligned-' + gene + '.aln'
                assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
                command = ClustalwCommandline(clustalw_exe, infile="./temp/unaligned.fasta", outfile = output)
                stdout, stderr = command()
                
                # read alignment file into ram 
                align = AlignIO.read(output, 'clustal')
                
                #print(align[0]) # mouse
                #print(align[1]) # dog
                #print(align[2]) # human
                
                # calculate edit distance # save human-mouse e-dist, human-canis e-dist 
                
                self.gene_edit_dist[gene] = {'human-mouse' : self.calculate_edit_distance(align[2], align[0]), 'human-dog' : self.calculate_edit_distance(align[1], align[2])}
            
            else: 
                print('failed to process: %s' % gene)
        
            with open('./data/edit_dists.pkl', 'wb') as f: 
                pickle.dump(self.gene_edit_dist, f)
                
        print('Finished calculating edit distances')
            
            
    def plot_conservation(self, species, recalc = False):
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
            self.get_edit_distances(self.group)
            
        DE_conserved = list(map(lambda x: self.gene_edit_dist[x][species], set(self.gene_edit_dist.keys()).intersection(self.DE_genes)))
        
        nonDE_conserved = list(map(lambda x: self.gene_edit_dist[x][species], set(self.gene_edit_dist.keys()).intersection(self.nonDE_genes)))
        
        cons = DE_conserved + nonDE_conserved
        dexp = ['DE']*len(DE_conserved) + ['non-DE']*len(nonDE_conserved)
        
        df = pd.DataFrame(data = {'conservation' : cons, 'DiffExp' : dexp } )
        
        fig1 = plt.figure()
        ax = sns.violinplot(x='DiffExp', y='conservation', data=df)
        
        fig1.suptitle(species)
        fig1.add_axes(ax)
        
        plt.show()
        
        manwhit = mannwhitneyu(DE_conserved, nonDE_conserved)
        
        print('Manwhitney test for species %s : %s' %(species.upper(), str(manwhit)))
    
class entrez_search_failure(Exception): 
    ''' 
    failure of search terms or connection
    ''' 
    
    def __str__(self): 
        return 'the entrez gene search failed to return a valid response' 




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
    

    tep.plot_conservation(species = 'human-mouse', recalc=False)
    

    tep.plot_conservation(species = 'human-dog')
    
