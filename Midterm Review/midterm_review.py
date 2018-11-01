# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:19:55 2018

@author: nathaniel 
@class: BMI650 
@HW: NA 
@title: Midterm review
"""

"""
Topics 
- Code Documentation
    # docstrings    
    # doc testing
    # PEP styles 
- Data types
    - Numerical, Sequence types, Dictionaries
        #Numerical: int, float, imaginary 
        #Sequence types: tuple (immutable) ,list (mutable) [] , string (immutable) str(), '', numpy array 
        #Dictionaries: Set of keys mapped to value object ... {} 
    - Mutable vs. Immutable
        # objects that can be modified after initialization are mutable 
        # mutable objects are passed by reference 
        # immutable objects are passed by copy 
        # immuatable data types: <int>, <float>, <str> <tuple> - others? 
        # mutable data types: <list>, <dict>, <set> - others?
""" 
_set = set() 
_dict = {} # or dict() 
_list = [] # or list() 
_tuple = (1,2,3) 

_set.add(1) 
_set.remove(1) 

_dict['new key'] = 420 
_dict['new key'] # 420 

_list.append('first')
_list.append('mid')
_list.append('end')
end = _list.pop() # comes off the end (end)
first = _list.pop(0)


        
"""
- Python operators
    - Operator precedence 
        # ??? mathamatical operators or logical operators ? 
    - String formatting
        # r'string' -> gives raw output ??? 
        # h'string' -> hexadecimal ??? 
        # 'here is a string, here is a string formater, %s' %'some string' 
        # 'another str, but with int: %d' %5 
        # 'last one, with float! %f' %4.34
        # 'just kidding, a double with truncated float: %s %.1f' % ('added string',3.333333333)
- Control structures 
    - if/else     
        # ... 
    - while and for loops
         # ... 
- List comprehension
    # wrapped in brackets: [<operation> for <handle> in <iterable> if <logic>]
    # there is also dictionary comprehension 
- File I/O
    # with open(path, 'w/r/a') as f: 
- Functions / generators (know the difference)
    # function is executed completely before returning, generators maintain a state and *yield* a value every time they are called. 
    # PRACTICE WITH THIS A BIT  
"""
def myGen(): 
    a = list( range(10) )
    
    while (len(a) > 0): 
        yield a.pop(0)
    
    yield -1

g = myGen()
for a in g: 
    print(a)

"""
- Modules
    # import xxx 
    # making your own module, make sure to add the: if __name__ == '__main__' : so as not to execute when imported. 
- Regular Expressions  
    # import re   
    - Groups
        # you can group your findings by components - PRACTICE THIS 
        # (...)
    - Sets
        # list functions 
    - Meta-characters (^, *, +, etc.)
        # These should be memorized. 
            # . : anything 
            # * : any number of repitions? 
            # ^ 
"""
print('---------------------')
import re
my_str_ = "+-0.01 % of people want ATTTCGGGCG to be in there bodyyyy IN MY BODDYYY" 
a = re.finditer('(?P<plus_minus>(?P<first>[+-]?)(?P<second>[+-]?))[0-9]*.[0-9]', my_str_)

for found in a: 
    print(found.group('plus_minus'))
    print(found.group('first'))
    print(found.group('second'))


            
"""            
- OOP / Classes and methods
    - Features of the OOP paradigm
        # a class has attributes and functions, can extend and inherit from other objects 
        - Inheritance, polymophism, encapsulation (mangling)
- Exceptions
    # assert logical "exception note" 
    # try, except 
    # 
    class myException(Exception): 
    '''This does not get printed, just doc string'''
        def __init__(self, vals_passed): 
            
            '''this only needs to be definied if your passing variables to use in __str__'''
        
        def __str__(self): 
            return 'this message'
    
    
    raise myException
    
- XML/HTML # yukkkkk <--------------------------------------------------------
    - Elementree
        # et.ElementTree() 
        # reading... # review this 
    - lxml
    - Basic Xpath syntax
"""

