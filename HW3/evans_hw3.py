# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 10:27:05 2018

@author: natha
@class: bmi665
#HW:3
"""

'''
XML and Python:
1) Download four UniProt (www.uniprot.org) XML files for the human proteins: ERBB1, ERBB2, ERBB3,
ERBB4
2) Write a Python program to extract Gene Ontology (GO) ID’s (e.g. “GO:0005524”) and term (e.g. “ATP
binding”) from each UniProt file using the ElementTree module. (6 points)
3) Write a function to create and write a table (tab delimited file) containing GO ID’s and terms in
common across all 4 proteins. The output file should have two columns, one for GO IDs and one for
GO terms. (2 points)
4) Write a function to create and write a table (tab delimited file) containing GO ID’s and terms in
common across at least 2 proteins. Make sure to include an additional column specifying the
associated proteins. The output file should have three columns: Protein names, GO ID, and GO term
(4 points).

Regular Expressions:
5) Write a Python program to extract the protein sequence from each protein's XML file (you may have
to remove spaces, newline characters, etc.). (4 points)
6) Translate the following PROSITE patterns into regular expressions, and write a function to search
each protein sequence for these sites. If matches are found, print out the matching sequence and
the location of each match to the screen. (4 points)
PROSITE Patterns:
Tyrosine protein kinases specific active-site signature (PS00109):
[LIVMFYC]-{A}-[HY]-x-D-[LIVMFY]-[RSTAC]-{D}-{PF}-N-[LIVMFYC](3)
Tyrosine kinase phosphorylation site (PS00007):
[RK]-x(2)-[DE]-x(3)-Y or [RK]-x(3)-[DE]-x(2)-Y
http://prosite.expasy.org/scanprosite/scanprosite_doc.html


'''

import xml.etree.ElementTree as ET
import os
import re


def full_search(root, att = ''):
    '''
    Search through all tree branches and only return nodes with given attribute (att) search paramaters. Use Xpath search notation. branch search ends when parameter is found 
    '''
    found = root.findall(att)
    if found: 
        return found
    ls = []
    for child in root: 
        # error when root is end branch? 
        l = full_search(child, att)
        if (l): # only add if non empty
            ls += l
    return ls
        
def parse_xml(): 
    fs = os.listdir('./data/xml/')
    f = './data/xml/' + fs[0]
    assert f[-4:] == '.xml', "trying to parse a non- xml file" 
    
    tree = ET.parse(f)
    root = tree.getroot()
    
    namespace = re.match(r"{.*}", root.tag).group()
    
    data = dict()
    for protein in root : 
        try: 
            name =  protein.find(namespace+"protein").find(namespace+"recommendedName").find(namespace+"fullName").text
            data[name] = {}

            data[name]["GO_IDS"] = full_search(protein, att="[@type='GO']") 
    
            data[name]["term_elements"] = full_search(protein, att="[@type='term']")
            
            data[name]["ids"] = {}
            
            for GO in data[name]["GO_IDS"] :
                data[name]["ids"][(GO.get('id'))] = GO[0].get("value")
            
            seq_elem = full_search(protein, att=namespace+"sequence")
            
            data[name]['seq'] = seq_elem[0].text.strip()
            #print( data[name]['seq'] )
            
        except: 
            print('failed to parse: ' + str(protein))
            
    return data


def analyze_ids(data): 
    
    all_ids = dict()
    # indice (i) represent set of ids shared among at least i+2 proteins 
    shared_id = [set()]*3
    for prot in data: 
        for goid in data[prot]["ids"]:
            term = data[prot]["ids"][goid]
            
            if goid not in all_ids.keys(): 
                all_ids[goid] = {'name': {prot}, 'term':term} 
            else: 
                all_ids[goid]['name'].add(prot)
                # add the id to shared membership group, so all ids in 2 are in 1 , 3 in 2... 
                #print(all_ids[goid]['name'])
                #print(len(all_ids[goid]['name']))
                shared_id[len(all_ids[goid]['name'])-2].add(goid)

    return (all_ids, shared_id)
    

def write_table(data, ids, identity_col=False, name=''):
    
    with open('./data/common_ids-' + name + '.csv','w') as f: 
        f.write('GO ID\tGO term')
        if(identity_col): 
            f.write('\tProtein Names\n')
        else: 
            f.write('\n')
            
        for goid in ids: 
            proteins = ','.join( data[goid]['name'] ) 
            term = data[goid]['term']
            f.write(goid + '\t' + term)
            if (identity_col): 
                f.write('\t' + proteins + '\n')
            else: 
                f.write('\n')
                     
            
                
'''
Tyrosine protein kinases specific active-site signature (PS00109):
[LIVMFYC]-{A}-[HY]-x-D-[LIVMFY]-[RSTAC]-{D}-{PF}-N-[LIVMFYC](3)
Tyrosine kinase phosphorylation site (PS00007):
[RK]-x(2)-[DE]-x(3)-Y or [RK]-x(3)-[DE]-x(2)-Y

down vote
Use a dictionary to look up the one letter codes:

d = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

'''
def seq_match(protein_name, seq, pattern = '', pattern_name='none given'):
    print('\n-----------------------------------')
    print('PROSITE CONVERTED SEQUENCE MATCHING - pattern id: ' + pattern_name )
    print('-----------------------------------')
    
    # make sure there are no unwanted characters 
    seq = re.sub('[^CIGADPHVSTLEQFRYKNWM]','', seq)
    
    matches = re.finditer(pattern, seq)
    
    print(protein_name + 'sequence pattern matches: ')
    for match in matches: 
        print('--------------------------------------')
        print('pattern match string: ' + match.group())
        print('pattern match indices (start, stop): ', match.span())

    print('No further matches found')
    

if __name__ == '__main__' :  
    
    # read data into dictionary with relevant parts 
    data = parse_xml() 
    
    # restructuring data and pre-computing shared ids
    goids, shared_ids = analyze_ids(data)
    
    # make table with common ids in all 4 proteins 
    write_table(goids, shared_ids[2], name='commontoall')
    
    # make table with common ids in at least 2 proteins 
    write_table(goids, shared_ids[0], name='commonto2proteins', identity_col=True)
    
    # prosite patterns 
   # (PS00007):
#[RK]-x(2)-[DE]-x(3)-Y or [RK]-x(3)-[DE]-x(2)-Y
    
    for prot in data: 
        seq_match(prot, data[prot]['seq'], pattern = '[LIVMFYC][^A][HY].D[LIVMFY][RSTAC][^D][^PF]N[LIVMFYC]{3}', pattern_name = 'PS00109')
        
        seq_match(prot, data[prot]['seq'], pattern = '[RK].{2}[DE].{3}Y | [RK].{3}[DE].{2}Y', pattern_name = 'PS00007')
    
    

