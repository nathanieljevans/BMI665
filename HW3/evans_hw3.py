# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 10:27:05 2018

@author: nathaniel evans
@class: bmi665
@HW:3

The instructions that prompted this script can be found at: 
    https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%203/BMI565_assignment3.pdf
    
    To run this script, it is necessary to have your desired xml file a relative path location: 
        /data/xml/
        
    The xml file in question should contain all the data that you wish to analyze, multiple xml files will result in only the first being analyzed. To combine your data into a single xml: 
        navigate to uniprot.org 
        search for relevant/desired proteins 
        click 'add to cart' 
            once all desired proteins are in the cart 
        click 'cart' 
        download all the files as an uncompressed xml to the relative (to this script) directory: 
                /data/xml/
                
        This script can then be run from command line by navigating to script folder location and using the command: 
            $python evans_hw3.py
            
        No additional arugments are required. 
        Output csv (tab delimited) files will be located in /data/ 
        Protein pattern matching will be written to the console. 
            This can be saved to a text file by adding command: 
                $python evans_hw3.py >> your_file.txt
"""

import xml.etree.ElementTree as ET
import os
import re


def full_search(root, att = ''):
    '''
    Search through all tree branches and only return nodes with given attribute (att)                   search paramaters. Use Xpath search notation. branch search ends when parameter is found 
    
    Args:
      root - ElementTree object denoting the root of the xml represented tree
      att (str) - the string to be searched for in branches
    Returns:
        ls [list of ElementTree objects] - all occurences that match the given pattern att
    '''
    
    found = root.findall(att)
    if found: 
        return found
    ls = []
    for child in root: 
        l = full_search(child, att)
        if (l): # only add if non empty
            ls += l
    return ls
        
def parse_xml(): 
    '''
    This function reads in the xml file, searches for the required data and stores it in a dictionary such that: 
            data {}
                key=protein_names -> 
                    dict {}
                        keys={"GO_IDS -> element tree objects for go ids
                              "term_elements" -> element tree objects for terms
                              "ids" ->
                                  dict {}
                                      keys={
                                            go-ids -> go_id-term_text
                                            }
                              "seq" -> protein sequence (str)
                              }
            
    Args:
        None
    Returns:
        data (dict) - data structure for relevant data, see above for keys
    '''
    
    fs = os.listdir('./data/xml/')
    f = './data/xml/' + fs[0]
    assert f[-4:] == '.xml', "trying to parse a non- xml file" 
    
    tree = ET.parse(f)
    root = tree.getroot()
    
    namespace = re.match(r"{.*}", root.tag).group()
    
    data = {}
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
            
        except: 
            #print('failed to parse: ' + str(protein))
            pass
            
    return data


def analyze_ids(data): 
    '''
    This function takes a data object defined in parse_xml() and creates two new data structures. One is a |list|=3 whose membership signifies at least [list index + 2] shared go id's. The second is a dictionary such that the key is the go id and the value is a dictionary with keys: 
                        'name' (set) - members are all proteins that share that go id
                        'term'
    
    Args:
        data (dict) - data structure to be analyzed
    Returns:
        all_ids - dict(keys=goid -> {keys('name','term')})
        shared_id = [{},{},{}]
        ids shared in 2  3  4   proteins - tiered such that 
                                            shared_id[1] in shared_id[0] -> True
    '''
    
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
                shared_id[len(all_ids[goid]['name'])-2].add(goid)

    return (all_ids, shared_id)
    

def write_table(data, ids, identity_col=False, name=''):
    '''
    writes table to a .csv file - tab delimited. Located in /data/
    
    Columns such that: 
        GO ID     GO term      Protein Names [optional]
        id...     term...      protein name(s)... (comma delimited)
        ...       ...          ....         
        
    Args:
     data (dict) - data to be written to table
     ids (list) - list of sets, membership signifies shared ids in at least i+2 proteins
     identity_col (boolean, default=False) - option to add Protein Names column 
     name (str, default='') - string to append to file name for uniqueness 
    Returns:
        None
    '''
    
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
                     
def seq_match(protein_name, seq, pattern = '', pattern_name='none given'):
    '''
    match given regular expression pattern (converted from prosite pattern) in given amino acid sequence. Print results to console. 
    
    Args:
      protein_name (str) - 
      seq (str) - aa sequence
      pattern (str) - regular expression pattern 
      pattern_name (str) - prosite pattern id
      
    Returns:
        None
    '''
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
    for prot in data: 
        # (PS00109):
        #[LIVMFYC]-{A}-[HY]-x-D-[LIVMFY]-[RSTAC]-{D}-{PF}-N-[LIVMFYC](3)
        seq_match(prot, data[prot]['seq'], pattern = '[LIVMFYC][^A][HY].D[LIVMFY][RSTAC][^D][^PF]N[LIVMFYC]{3}', pattern_name = 'PS00109')
        
        # (PS00007):
        #[RK]-x(2)-[DE]-x(3)-Y or [RK]-x(3)-[DE]-x(2)-Y
        seq_match(prot, data[prot]['seq'], pattern = '[RK].{2}[DE].{3}Y | [RK].{3}[DE].{2}Y', pattern_name = 'PS00007')
    
    

