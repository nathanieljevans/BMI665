# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:54:51 2018

@author: nathaniel evans
@class: BMI665 
@HW: 4 


Assignment #4
Submit source code and write-up (including program output) through Sakai.
BMI 565/665 Bioinformatics Programming and Scripting
1) Create a custom exception definition that can be raised when a sequence is something other than
DNA (e.g., an mRNA or protein sequence). Call this exception "SeqTypeError".
2) Using either lxml or BeautifulSoup, extract the nucleotides represented by the IUPAC nucleotide
codes W, S, M, K, R, and Y from the table in the following Wikipedia page (assume you know that N
means any nucleotide: A, T, C or G). Store this information in a dictionary and use the info to create
the regular expressions for the recognition sites listed in (3) below:
https://en.wikipedia.org/wiki/Nucleic_acid_notation
3) Create a Class definition for DNA sequence data with the following features:
- a class attribute called ResEnzymeDict, which is a dictionary of restriction enzymes and their
recognition sites (as regular expression patterns).
- an instance attribute to hold a DNA sequence
- The user will be alerted if the sequence is not DNA (using the exception created above).
- a method, called "restriction_sites" that searches the DNA sequence for the restriction enzyme
recognition sites (using regular expressions), and prints out those enzymes whose recognition sites
exist in the DNA sequence along with the sequence that matched the recognition site pattern.
The ResEnzymeDict attribute should contain the following enzymes and recognition sites:
EcoRI: GAATTC
EalI: YGGCCR
ErhI: CCWWGG
EcaI: GGTNACC
FblI: GTMKAC
Deliverables:
- Code for 1, 2 and 3 in a single file
- Write-up of results
"""

from bs4 import BeautifulSoup 
import urllib.request as url 
import re

WIKI_URL = "https://en.wikipedia.org/wiki/Nucleic_acid_notation" 

class SeqTypeError(Exception): 
    '''Sequence is not valid DNA representation''' 
    pass 
    

def parse_table(table, kbs_to_extract): 
    '''
    return set of kbs that it represents and the complement
    
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
    ResEnzymeDict = {
            'EcoRI': 'GAATTC',
            'EalI': 'YGGCCR',
            'ErhI': 'CCWWGG',
            'EcaI': 'GGTNACC',
            'FblI': 'GTMKAC',
            }
    
    def __init__(self, DNA, codex): 
        if not re.sub('[ATCG]', '', DNA) == '': raise SeqTypeError()
        
        self.codex = codex # extracted table info 
        self.DNA = DNA 
    
    def __generate_re_patterns__(self): 
        self.ResEnzymeRE = {}
        for name in self.ResEnzymeDict: 
            codified_pattern = self.ResEnzymeDict[name]
            pattern = ''
            for kb in codified_pattern: 
                pattern += "[" + set_to_string(self.codex[kb]['base_rep']) + "]"
            self.ResEnzymeRE[name] = pattern
        
        return self.ResEnzymeRE
    
    def restriction_sites(self): 
        self.__generate_re_patterns__()
        for name in self.ResEnzymeRE: 
            srch = re.finditer(self.ResEnzymeRE[name],self.DNA)
            
            output = '------------------------------------------------------\n'
            output+= 'DNA pattern match(es) to code: ' + name + '\n'
            for find in srch: 
                output+='index span: ' + str(find.span(0)) + '\n'
                output+='DNA sequence match: ' + str(find.group(0)) + '\n'
            output += '-------------------------------------------------------'
            
            # had a very difficult time finding any sleek way to check if an interable object is empty or not, so this is my work around to only print the objects that are not empty. Bit wasteful, but easy implementation. 
            if (len(output) > 146) : 
                print(output)

def set_to_string(_set): 
    s = ''
    for item in _set: 
        s += str(item)  
    return s
    


if __name__ == "__main__" : 
    # main script 
    
    ## part 2, extract table and store info 
    html = url.urlopen(WIKI_URL).read() # pull html and read into memory 
    NAN = BeautifulSoup(html, 'lxml')
    NAN.prettify() 
    tables = NAN.find_all('table')

    # parse the data and add intuitive knowledge about N 
    tbl_data = parse_table(tables[0], {'W', 'S', 'M', 'K', 'R', 'Y', 'N', 'A', 'C', 'G', 'T'} )
    print(tbl_data)
    
    mySeq = DNA_SEQ('GATTACAGAATTCTTTTTTGAATTC',tbl_data)
    mySeq.restriction_sites()
    print(mySeq.ResEnzymeRE)
    
            
    
    
    
