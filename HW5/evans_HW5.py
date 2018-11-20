# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:23:05 2018

@author: nathaniel evans
@class: BMI665 
@prof: mike mooney 
@date: 11/6/2018 
@HW: 5 

This module can be imported or run in console by navigating to the appropriate directory and using the command: 
    $ python evans_HW5.py 
    
There must be a ./data directory with the script. 

Be careful using these methods to create or work with graphs > 10K nodes as memory and search traversals will take substantial memory and compute time. 
"""

import networkx as nx 
import random as rand 
from matplotlib import pyplot as plt 

def create_graph(num_nodes = 10, connectivity=0.25):
    '''
    Generate a random graph in O(n^2)
    
    input 
        num_nodes <int> number of nodes to be included in the graph 
        connectivity <float> probability of being connected to any other node 
    
    output
        G <networkx graph> graph with num_nodes and liklihood to be connected with any other node of connectivity*100
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
    
    input 
        p <float> [0,1] the probability that a node is connected to each different node. 
    
    output 
        <boolean> True, stochasticly determined connection
    '''
    if (rand.random() < p): 
        return True
    else: 
        return False

def depth_search(G, current, visited = None): 
    '''
    recursive depth first search starting at a given node 
    
    inputs
        G <networkx> graph to search 
        current <int> node identifier currently at 
        visited <set> nodes that have been visited 
        
    outputs 
        <node_order> nodes of graph G in order they were visited. 
    '''
    
    if (not visited): 
        visited = set()
    #visited.clear() # without this, multiple calls will fail. Why is visited not reset after the method finishes? The namespace should collapse once the function finishes, right? <-- I'd actually like to discuss this 
    
    node_order = [current]
    visited.add(current)
    
    for node in G.neighbors(current): 
        if node not in visited : 
            node_order = depth_search(G,current=node, visited=visited) + node_order

    return node_order

def breadth_search(G, start): 
    '''
    breadth first search of a graph 
    
    input 
        G <networkx graph> graph to be searched 
        start <int> node to start at
        
    output
        order <list> list of int representing order (by index) of the nodes visited 
    '''

    order = [start]
    visited = set([start])
    i=0
    
    while(i<len(order)): 
        children = set([x for x in G.neighbors(order[i])]) - visited 
        order += [x for x in children]
        visited = visited.union( children )
        i+=1 
        
    return order

def save_graph(G, path='./output/', name = 'random_graph'): 
    '''
    saves a graph plot to file. 
    
    input 
        G <networkx graph> graph to be drawn and saved 
        path <str> path to save the output, default is one folder down named output.
        
    output 
        None 
    '''
    
    f = plt.figure() 
    nx.draw(G,with_labels=True, ax = f.add_subplot(111))
    plt.savefig(path + name + '.png') 
    # plt, this should get cleared before the next 
    plt.clf()
    
def is_connected(G): 
    ''' 
    Checks a graph to see if it's fully connected (any node can be traversed to any other node)
    
    input 
        G <networkx graph> G to check connectivity 
    
    output
        <boolean> True -> fully connected 
    '''
    order = depth_search(G,0)
    if len(order) < len(G): 
        return False
        
    return True

if __name__ == '__main__' : 
    G = create_graph(num_nodes=10, connectivity=.2)
    
    print('depth first search:', depth_search(G, 0))
    
    print('breadth first search:', breadth_search(G, 0))
    
    print('graph is connected:', is_connected(G)) 
    
    save_graph(G)
    
    G2 = nx.karate_club_graph() 
    
    print('[karate club] depth first search:\n', depth_search(G2, 0))
    
    print('[karate club] breadth first search:\n', breadth_search(G2, 0))
    
    print('[karate club] graph is connected:', is_connected(G2)) 
       
    plt.clf()
    nx.draw(G2, with_labels=True)
    
    # test connectivity 
    #print((len(create_graph(num_nodes=100, connectivity=0.75).edges())*2) / 100e3)
    
    
    