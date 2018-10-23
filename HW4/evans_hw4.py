# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:54:51 2018

@author: nathaniel evans
@class: BMI665 
@HW: 4 

This program can be run from bash command line using the command: 
    $ python evans_hw4.py <DNA-seq-string> 
    eg. 
    $ python evans_hw4.py "GATTACA" 
    
    Alternatively, running without an argument will result in a default DNA seq test. 
    
    The purpose of this script is to:
        A. Read in the IUPAC codes from the url: 
            https://en.wikipedia.org/wiki/Nucleic_acid_notation
        B. Analyze a user provided DNA sequence and print to console any restriction enzyme sites that are found. 
        
    If the provided DNA sequence contains characters other than [ATCG] a SeqTypeError will be thrown. 
            
"""

from bs4 import BeautifulSoup 
import urllib.request as url 
import re
import sys

#url to extract pattern conversion data 
WIKI_URL = "https://en.wikipedia.org/wiki/Nucleic_acid_notation" 

# exception to be thrown if a DNA sequence representation is misrepresented
class SeqTypeError(Exception): 
    '''Sequence is not valid DNA representation''' 
    pass 
    
def parse_table(table, kbs_to_extract): 
    '''
    Given a table, extract the desired information and return as a dictionary. 
    
    input
        table <bs4.element.tag> beautiful soup object representing the table to be parsed 
        kbs_to_extract <set<str>> set of single char strings to extract info
        
    output 
        tbl_dic <dictionary> data with keys = kbs_to_extract and second level keys: base_rep and compliment 
    '''
    tbl_dic = {} 
    for row in table.find_all('tr')[1:]: # only one table to grab 
        kb = row.find('td').string 
        
        if kb in kbs_to_extract: 
            tbl_dic[kb] = {'base_rep':set(), 'complement':row.find_all('td')[-1].string.strip()} 
            for j, textO in enumerate(row.find_all('td')[2:6]): 
                text = textO.string
                if (text is not 'None' and text is not None):
                    tbl_dic[kb]['base_rep'].add(text)
    return tbl_dic



class DNA_SEQ: 
    ''' 
    This class represents a DNA sequence and can be used to find any given matching Restriction Enzyme sites. A dictionary condex is needed to convert IUPAC codes to regular expression patterns, should you wish to interpret these patterns differently, a custom codex dictionary can be passed in.
    '''
    
    ResEnzymeDict = {
            'EcoRI': 'GAATTC',
            'EalI': 'YGGCCR',
            'ErhI': 'CCWWGG',
            'EcaI': 'GGTNACC',
            'FblI': 'GTMKAC',
            }
    
    def __init__(self, DNA, codex): 
        '''
        initialize the DNA_SEQ object
        
        inputs 
            DNA<str> sequence representing one strand of DNA, must only include characters [ATCG]
            codex<dict> dictionary mapping IUPAC codes to re expressions, for syntax, use help(parse_table)
            
        outputs
            None
        '''

        if not re.sub('[ATCG]', '', DNA) == '': raise SeqTypeError() # make sure only ATCG values are present in seq
        
        self.codex = codex # extracted table info 
        self.DNA = DNA 
    
    def __generate_re_patterns__(self): 
        '''
        convert IUPAC restriction enzyme patterns to RE pattern using instance provided codex. 
        
        inputs
            None
        outputs
            None
        '''
        self.ResEnzymeRE = {}
        for name in self.ResEnzymeDict: 
            codified_pattern = self.ResEnzymeDict[name]
            pattern = ''
            for kb in codified_pattern: 
                pattern += "[" + set_to_string(self.codex[kb]['base_rep']) + "]"
            self.ResEnzymeRE[name] = pattern

    
    def restriction_sites(self): 
        '''
        Searches instance DNA sequence for subsequences that match the provided IUPAC patterns. When a match is found, it is printed to console. 
        
        inputs 
            None
        
        ouputs
            None
        '''
        self.__generate_re_patterns__()
        for name in self.ResEnzymeRE: 
            srch = re.finditer(self.ResEnzymeRE[name],self.DNA)
            
            output = '------------------------------------------------------\n'
            output+= 'DNA pattern match(es) to code: ' + name + '\n'
            for find in srch: 
                output+='index span: ' + str(find.span(0)) + '\n'
                output+='DNA sequence match: ' + str(find.group(0)) + '\n'
            output += '-------------------------------------------------------'
            
            # had a very difficult time finding any sleek way to check if an interable object is empty or not, so this is my work around to only print the objects that are not empty. It's a bit wasteful, but easy to implement. 
            
            if (len(output) > 175) : 
                print(output)

def set_to_string(_set): 
    '''
    convert set of chars to string without syntax
    
    input
        _set<set> chars to be converted to string 
        
    output
        s<str> string of set chars
    '''
    
    s = ''
    for item in _set: 
        s += str(item)  
    return s
    

'''
executed script 
'''
if __name__ == "__main__" :  
    
    ## part 2, extract table and store info 
    html = url.urlopen(WIKI_URL).read() # pull html and read into memory 
    NAN = BeautifulSoup(html, 'lxml')
    NAN.prettify() 
    tables = NAN.find_all('table')

    # parse relevant data
    tbl_data = parse_table(tables[0], {'W', 'S', 'M', 'K', 'R', 'Y', 'N', 'A', 'C', 'G', 'T'} )
    
    # seq data input method 
    if (len(sys.argv) > 1): 
        DNA = sys.argv[1]
    else: #    EcoRI ------EalI --------ErhI ---------- EcalI -------- FblI
        DNA = "GAATTCAAAAAACGGCCAAAAAAAAACCTTGGAAAAAAAAGGTAACCAAAAAAAAAGTATAC"
        print('test case, seq used: ' + DNA)
            
    # anaylze data
    mySeq = DNA_SEQ(DNA, tbl_data)
    mySeq.restriction_sites()

    
            
    
    
    
