import sys
import unittest
from typing import TypeAlias, Optional, Callable, Any
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

# Value type stored in the BST
Value : TypeAlias = Any

# Binary tree type definition
BinTree : TypeAlias = Optional['Node']

# Comparator type definition - more precise typing
Comparator : TypeAlias = Callable[[Value, Value], bool]

# Helper type aliases for clarity (defined after BinarySearchTree class)
ComparisonResult : TypeAlias = bool

# Node in a binary search tree
@dataclass(frozen=True)
class Node:
    value: Value
    left: BinTree
    right: BinTree

# Data definition for a binary search tree
@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Comparator
    tree: BinTree

# Short alias for convenience
BST : TypeAlias = BinarySearchTree
    
# Returns True if 'BST' is empty, False otherwise.
def is_empty(BST: BST) -> bool:
    if BST.tree is None:
        return True
    return False

# Insert 'value' into 'BST', returning the new BST.
def insert(BST: BST, value: Value) -> BST:
    comes_before = BST.comes_before
    
    # Helper function to recursively insert the value
    def insert_helper(tree: BinTree) -> BinTree:
        if tree is None:
            return Node(value, None, None)
            
        is_less: ComparisonResult = comes_before(value, tree.value)
        is_greater: ComparisonResult = comes_before(tree.value, value)
        
        if is_less:
            return Node(tree.value, insert_helper(tree.left), tree.right)
        elif is_greater:
            return Node(tree.value, tree.left, insert_helper(tree.right))
        else:
            # Values are equal, don't insert duplicates
            return tree
        
    return BinarySearchTree(comes_before, insert_helper(BST.tree))

# Returns True if 'value' is in 'BST', False otherwise.
def lookup(BST: BST, value: Value) -> bool:
    comes_before = BST.comes_before

    # Helper function to recursively search for the value
    def lookup_helper(tree: BinTree) -> bool:
        if tree is None:
            return False
        
        is_less = comes_before(value, tree.value)
        is_greater = comes_before(tree.value, value)
        
        if is_less:
            return lookup_helper(tree.left)
        elif is_greater:
            return lookup_helper(tree.right)
        else:
            # Values are equal, so value already exists
            return True
        
    return lookup_helper(BST.tree)


# Return the largest value in the non-empty 'tree'.
def largest_value(tree: BinTree) -> Value:
    match tree:
        case None:
            raise ValueError("tree is empty.")
        case Node(v, l, r):
            if r is None:
                return v
            return largest_value(r)
        

# Delete the largest value in the non-empty 'tree'.
def delete_largest_value(tree: BinTree) -> BinTree:
    match tree:
        case None:
            raise ValueError("tree is empty.")
        case Node(v, l, r):
            if r is None:
                return l
            else:
                new_r : BinTree = delete_largest_value(r)
                return Node(v, l, new_r)

# Delete the root of 'tree'
def delete_root(tree: BinTree) -> BinTree:
    match tree:
        case None:
            return None
        case Node(v, l, r):
            # Get the largest value "left_max" out of "l".
            # Make a new version of "l" where left_max has been removed from it
            # Return a new BST where left_max is the new root value, and 
            #   where the new version of 'l' is used (right subtree unaffected)
            if l is None:
                return r
            else:
                left_max: Value = largest_value(l)
                new_left_subtree: BinTree = delete_largest_value(l)
                return Node(left_max, new_left_subtree, r)

# Delete 'value' from 'BST' (if present)
def delete(BST: BST, value: Value) -> BST:
    value_present = lookup(BST, value)
    
    if value_present is False:
        return BST
    
    comes_before = BST.comes_before
    tree = BST.tree
    
    # Helper function to recursively delete the value
    def delete_helper(currentTree: BinTree, v: Value) -> BinTree:
        match currentTree:
            case None:
                return None
            case Node(root_v, l, r):
                is_less = comes_before(v, currentTree.value)
                is_greater = comes_before(currentTree.value, v)
                
                if is_less:
                    return Node(root_v, delete_helper(l, value), r)
                elif is_greater:
                    return Node(root_v, l, delete_helper(r, value))
                else:
                    # found the value
                    return delete_root(currentTree)
    
    return BinarySearchTree(comes_before, delete_helper(tree, value))