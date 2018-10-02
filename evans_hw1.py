# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:56:12 2018

@author: nathaniel evans
BMI665: Scripting 
Homework # 1
"""

'''
Assignment #1
Submit source code and write-up (including program output) through Sakai.
BMI 565/665 Bioinformatics Programming and Scripting
Work through the “Getting Started” tutorial available on Sakai.
Install Python (preferably Anaconda), and download/clone the Github repo with class materials (1 point)
Chapter 2:
1) What is a comment in source code? Give two reasons for using comments. (2 point)
'''
    # comments are used to document your code, they explain what your functions do and why, briefly. 
    # Two reasons to document your code are 1) to make it readable by other programmers and 2) to 
    # remind yourself what you were trying to accomplish and how. 

'''
2) What is a “shebang” or “hashbang”? (1 point)
    '''
    # shebang is a character sequence ( #! ) at the begginning of a unix (usually) script that specifies
    # the interpreter that should be used to run the remaining file as an executable. The shebang is 
    # followed by the path to your interpreter eg. usr/bin/python 
    
'''    
Chapter 3: Data types
3) What is a python dictionary? Describe in two sentences. (2 points)
    '''
    # a python dictionary is an object that maps an key to a value. The key can be any immutable 
    # object and the value can any object. Implementation can be done as follows: 
    # dict_obj = {'key':['value','object',123]}

# coding component -----------------------------------------------------------
'''
4) Write a program that converts temperature in Fahrenheit to Celsius and use string formatting to
write the result with one decimal value (e.g. 75.2 degrees Celsius). Use this formula to make the
conversion: Tc = (5/9) * (Tf – 32). The program should take user input (hint: see the raw_input()
function) and write results to the screen. (4 points)
'''

def FtoC(F): 
    '''
    Given a temperature in F, prints temp in C to console and returns Tc
    
    Args:
    param1 (float): Temperature in farenheight
    
    Returns:
    float : Temperature in celcius 
    '''
    
    C = 5/9*(F-32)
    print("Temperature F, C" , [F,C])
    return (C)

FtoC(45)

'''
Chapter 4: Flow control
5) Write a program that uses a loop to create a list of random rolls of a die (i.e., numbers between 1
and
6) of a specified length. The program should ask the user for the number of rolls, and then print
the list of rolls to the screen. (4 points)
'''
import random as rand
def FlowControl(): 
    '''
    Rolling a dice a user specified number of times 
    
    Args:
        None
    
    Returns:
        list<int> : Random sequence of rolls of user specified length 
    '''
    l = int(input("How many times shall we roll the dice? "))
    print(type(l))
    assert type(l) == type(int(1)) and l > 0 , "please enter and integer greater than 0" 
    r = []
    for i in range(l):
        r.append(rand.randint(1,6))
    print("our list of rolls: " , r)
    return r 

FlowControl()

'''
List Comprehension Exercises: (2 points each)
6) Use list comprehension to create the same list described in #5 above.
'''

def FlowControl_lc(): 
    '''
    Rolling a dice a user specified number of times using list comprehension
    
    Args:
        None
    
    Returns:
        list<int> : Random sequence of rolls of user specified length 
    '''
    l = int( input("How many times shall we roll the dice? ") )
    assert (type(l) == int) and (l > 0) , "please enter and integer greater than 0" 
    rolls = [rand.randint(1,6) for x in range(l)]
    print("dice rolls in list: ", rolls)
    return rolls 

'''
7) Use list comprehension to count the number of rolls greater than 3 in the list created above.
'''
sums = sum([x for x in FlowControl_lc() if x > 3])

'''
    
8) Given a DNA sequence, use list comprehension to create a list that stores the positions (indexes) of
every 'T' in the sequence. For example, if the sequence is "ATCGAATT", the resulting list would be:
[1, 6, 7].
'''
import re
def T_position(DNA):
    '''
    Returning the indices of all T's in a given DNA seq (ATCG)
    
    Args:
        (str) DNA : sequence representing DNA
    
    Returns:
        list<int> : list denoting the indices of each T occurence in the given DNA sequence 
    '''
    assert type(DNA) == type('') and len(DNA) > 0 and len(re.sub(r'[ATCG]', '', DNA)) == 0, "DNA seq input should be a non-empty string consisting of only ATCG's"
    inds = [i for i,x in enumerate(DNA) if x=='T']
    print("Index positions of all Ts in seq (First few kbs: " + DNA[0:10] + "): ", inds)
    return inds 

T_position("ATCGAATT")

'''
** Remember to include comments at the top of your code, as described in the lecture notes (with your
name, the assignment number, etc.), and to name your files appropriately (e.g. LastName_hw1.doc,
LastName_hw1.py, etc.).
'''