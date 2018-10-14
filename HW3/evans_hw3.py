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
        

    


if __name__ == '__main__' :  
    
    fs = os.listdir('./data')
    f = './data/' + fs[0]
    
    tree = ET.parse(f)
    root = tree.getroot()
    
    namespace = re.match(r"{.*}", root.tag).group()
    print(namespace)
    
    data = dict()
    for protein in root : 
        try: 
            name = prot_tag = protein.find(namespace+"protein").find(namespace+"recommendedName").find(namespace+"fullName").text
        except: 
            print('failed to parse: ' + str(protein))

        data[name] = {"GO_IDS" : full_search(protein, att="[@type='GO']") } 
        print(data[name]["GO_IDS"])
        data[name] = {"term_elements" : full_search(protein, att="[@type='term']")}

        data[name]["ids"] = []
        for GO in data[name]["GO_IDS"] : 
            data[name]["ids"].append(GO.get('id'))
            
        data[name]['term'] = []
        for t in data[name]["term_elements"]: 
            data[name]['term'].append( t.get('value') ) 
            
        
            
    
    print (data)

