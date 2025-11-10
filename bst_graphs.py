import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import numpy as np
import random
sys.setrecursionlimit(10**6)

from bst import *

TREES_PER_RUN : int = 10000

#  takes in an integer n and generates a BinarySearchTree
# containing n random floats in [0,1].
def random_tree(n: int, comes_before: Comparator) -> bst:
    """ Returns a random binary search tree with 'n' nodes,
        using 'comes_before' as the comparator function.
    """
    tree : bst = BinarySearchTree(comes_before, None)
    for _ in range(n):
        value : float = random.random() # random float in [0,1)
        tree = insert(tree, value)
    return tree

# Returns the height of the binary search tree 'tree'.
def calculate_tree_height(tree: BinTree) -> int:
    """ Returns the height of the binary tree 'tree'. """
    if tree is None:
        return 0
    left_height : int = calculate_tree_height(tree.left)
    right_height : int = calculate_tree_height(tree.right)
    return 1 + max(left_height, right_height)

# comes_before func on that relies on standard < behavior
def default_comparator(x: Value, y: Value) -> bool:
    return x < y

# Experimentally determine a value of n_max such that performing the 
# following TREES_PER_RUN times takes about 1.5–2.5 seconds: generate 
# a random tree of size n_max and compute its height.
def find_n_max_height() -> int:
    n_max : int = 1
    comes_before : Comparator = default_comparator
    while True:
        import time
        start_time : float = time.time()
        
        for _ in range(TREES_PER_RUN):
            tree : bst = random_tree(n_max, comes_before)
            _ = calculate_tree_height(tree.tree)
            
        end_time : float = time.time()
        total_time : float = end_time - start_time
        average_time : float = total_time / TREES_PER_RUN
        
        print(f"n_max={n_max}, total_time={total_time:.4f} seconds, average_time={average_time:.4f} seconds")
        if 1.5 <= total_time <= 2.5:  # Check total time, not average
            break
        n_max *= 2
        
    print(f"Chosen n_max: {n_max}")
    return n_max

# Experimentally determine a value of n_max such that performing the 
# following TREES_PER_RUN times takes about 1.5–2.5 seconds: generate 
# a random tree of size n_max by inserting n_max random values.
def find_n_max_insert() -> int:
    n_max : int = 1
    comes_before : Comparator = default_comparator
    while True:
        import time
        start_time : float = time.time()
        
        for _ in range(TREES_PER_RUN):
            tree : bst = BinarySearchTree(comes_before, None)
            for _ in range(n_max):
                value : float = random.random()
                tree = insert(tree, value)
                
        end_time : float = time.time()
        total_time : float = end_time - start_time
        average_time : float = total_time / TREES_PER_RUN
        
        print(f"n_max={n_max}, total_time={total_time:.4f} seconds, average_time={average_time:.4f} seconds")
        if 1.5 <= total_time <= 2.5:  # Check total time, not average
            break
        n_max *= 2
        
    print(f"Chosen n_max for insert: {n_max}")
    return n_max

# Make a graph of average tree height (y axis) as a func on of N (x axis). 
# Use 50 different N samples spaced evenly from N=0 to N=n_max. At each N
# find the average height of TREES_PER_RUN random trees of size N.
def create_height_graph(n_max: int) -> None:
    n_samples : int = 50
    comes_before : Comparator = default_comparator
    x_coords : List[float] = []
    y_coords : List[float] = []
    
    for i in range(n_samples + 1):
        n : int = (i * n_max) // n_samples
        total_height : int = 0
        for _ in range(TREES_PER_RUN):
            tree : bst = random_tree(n, comes_before)
            height : int = calculate_tree_height(tree.tree)
            total_height += height
        average_height : float = total_height / TREES_PER_RUN
        x_coords.append(float(n))
        y_coords.append(average_height)
    
    x_numpy : np.ndarray = np.array(x_coords)
    y_numpy : np.ndarray = np.array(y_coords)
    plt.plot(x_numpy, y_numpy, label='Average Tree Height')
    plt.xlabel("Number of Nodes (N)")
    plt.ylabel("Average Height")
    plt.title("Average Height of Random BSTs vs Number of Nodes")
    plt.grid(True)
    plt.legend() # makes the 'label's show up
    plt.show()
    
def create_insert_graph(n_max: int) -> None:
    n_samples : int = 50
    comes_before : Comparator = default_comparator
    x_coords : List[float] = []
    y_coords : List[float] = []
    
    for i in range(n_samples + 1):
        n : int = (i * n_max) // n_samples
        total_time : float = 0.0
        
        for _ in range(TREES_PER_RUN):
            # First, create a tree of size n
            tree : bst = random_tree(n, comes_before)
            
            # Then time inserting ONE additional random value
            import time
            start_time : float = time.time()
            value : float = random.random()
            tree = insert(tree, value)
            end_time : float = time.time()
            
            total_time += (end_time - start_time)
            
        average_time : float = total_time / TREES_PER_RUN
        
        x_coords.append(float(n))
        y_coords.append(average_time)
    
    x_numpy : np.ndarray = np.array(x_coords)
    y_numpy : np.ndarray = np.array(y_coords)
    plt.plot(x_numpy, y_numpy, label='Average Single Insert Time')
    plt.xlabel("Tree Size (N)")
    plt.ylabel("Average Time to Insert One Value (seconds)")
    plt.title("Time to Insert Single Value into BST vs Tree Size")
    plt.grid(True)
    plt.legend()
    plt.show()

def create_bst_graphs() -> None:    
    print("Finding n_max for insert timing...")
    n_max = find_n_max_insert()
    create_insert_graph(n_max)
    
    return
    
    
if (__name__ == '__main__'):
    create_bst_graphs()