# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:23:05 2018

@author: natha
"""

import networkx as nx 
import random as rand 

'''
Assignment #5
Submit source code and write-up (including program output) through Sakai.
BMI 565/665 Bioinformatics Programming and Scripting 
Create a single module that contains the following three functions:
1) A function to create a random graph. This function will take a single parameter for the number
of nodes in the graph, and will return a NetworkX undirected graph object.
'''
def create_graph(num_nodes = 10, connectivity=0.75):
    '''
    Generate a random graph in O(n^2)
    
    test average connectivity 
    >>> 0.55 > (len(create_graph(num_nodes=1000, connectivity=0.5).edges()) / 1000) > 0.45
    
    input 
        num_nodes <int> number of nodes to be included in the graph 
        connectivity <float>
    '''
    G = nx.Graph() 
    for i in range(num_nodes): 
        G.add_node(i, label=i) 
        
        for node in G: 
            if node != i and rand_connect(connectivity):
                G.add_edge(i, node)
    return G
            
        
    
def rand_connect(p): 
    ''' 
    return 0/1 depending on probability, p refers to 1. 
    '''
    if (rand.random() < p): 
        return True
    else: 
        return False


'''
2) A function that implements a depth-first search of a graph. This function will take two
parameters: a NetworkX graph object and the node at which to start the search. It will return a
list of node names in the order they were visited. (Hint: use a stack to implement this algorithm)
'''
# ??? DOUBLE CHECK THAT THIS IS ACTUALLY DEPTH FIRST ORDER 
def depth_search(G, current=None, visited = set()): 
    '''
    depth first search starting at a given node 
    
    inputs
        G <networkx> graph to search 
        current <int> node identifier currently at 
        visited <set> nodes that have been visited 
        
    outputs 
        <node_order> nodes of graph G in order they were visited. 
    '''
    node_order = [current]
    visited.add(current)
    for node in G.neighbors(current): 
        if node not in visited : 
            node_order = depth_search(G,current=node, visited=visited) + node_order
            
    return node_order


'''
3) A function that implements a breadth-first search of a graph. This function will take two
parameters: a NetworkX graph object and the node at which to start the search. It will return a
list of node names in the order they were visited. (Hint: use a queue to implement this
algorithm)
Use the module to do the following:
4) Create and draw a random graph with 10 nodes (show the node labels on the drawing and save
the figure to a file).
5) Run a depth-first search on the random graph. Show the order in which the nodes were visited.
6) Run a breadth-first search on the random graph. Show the order in which the nodes were
visited.
7) Use either search algorithm to determine whether the random graph is connected (DON’T use
the NetworkX is_connected() function).
8) Also, do 5 through 7 above using the example karate club graph shown in class (start at node 0).
Deliverables:
1. A Python module containing the functions specified above.
2. A word document showing the commands for importing and using the module, along with the
output for 4-8 above (please paste the figure of the random graph in this document).

'''

if __name__ == '__main__' : 
    
    print('a')
    G = create_graph(num_nodes=10, connectivity=.25)
    
    print('made it here')
    order = depth_search(G, current=1)
    print(order)
    
    nx.draw_circular(G,with_labels=True)
    
    # test connectivity 
    #print((len(create_graph(num_nodes=1000, connectivity=0.75).edges())*2) / 1000e3)
    
    
    