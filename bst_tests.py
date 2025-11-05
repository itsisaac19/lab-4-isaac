import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
sys.setrecursionlimit(10**6)

from bst import *

# Point class for Euclidean distance testing
@dataclass(frozen=True)
class Point2:
    x: float
    y: float
    
    def distance_from_zero(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

class BSTTests(unittest.TestCase):
    
    def test_integer_ordering(self):
        """Test BST with basic numeric ordering of integers"""
        def int_comes_before(a: int, b: int) -> bool:
            return a < b
        
        # Create empty BST
        bst = BinarySearchTree(int_comes_before, None)
        self.assertTrue(is_empty(bst))
        
        # Insert values
        values = [5, 3, 7, 1, 4, 6, 9, 2, 8]
        for val in values:
            bst = insert(bst, val)
        
        self.assertFalse(is_empty(bst))
        
        # Test lookup - all inserted values should be found
        for val in values:
            self.assertTrue(lookup(bst, val))
        
        # Test lookup - values not inserted should not be found
        self.assertFalse(lookup(bst, 0))
        self.assertFalse(lookup(bst, 10))
        self.assertFalse(lookup(bst, -1))
        
        # Test duplicate insertion (should not change BST)
        original_tree = bst.tree
        bst_with_dup = insert(bst, 5)  # 5 already exists
        self.assertEqual(bst_with_dup.tree, original_tree)
        
        # Test deletion
        bst = delete(bst, 5)  # Delete root
        self.assertFalse(lookup(bst, 5))
        self.assertTrue(lookup(bst, 3))  # Other values still there
        
        bst = delete(bst, 1)  # Delete leaf
        self.assertFalse(lookup(bst, 1))
        
        bst = delete(bst, 7)  # Delete node with children
        self.assertFalse(lookup(bst, 7))
        
        # Delete non-existent value (should not change BST)
        bst_unchanged = delete(bst, 100)
        self.assertEqual(bst.tree, bst_unchanged.tree)
    
    def test_string_alphabetic_ordering(self):
        """Test BST with alphabetic ordering of strings"""
        def string_comes_before(a: str, b: str) -> bool:
            return a < b
        
        # Create empty BST
        bst = BinarySearchTree(string_comes_before, None)
        self.assertTrue(is_empty(bst))
        
        # Insert string values
        words = ["dog", "cat", "elephant", "ant", "bear", "fox", "zebra"]
        for word in words:
            bst = insert(bst, word)
        
        self.assertFalse(is_empty(bst))
        
        # Test lookup
        for word in words:
            self.assertTrue(lookup(bst, word))
        
        # Test lookup for non-existent strings
        self.assertFalse(lookup(bst, "horse"))
        self.assertFalse(lookup(bst, ""))
        self.assertFalse(lookup(bst, "aardvark"))
        
        # Test case sensitivity
        bst = insert(bst, "Dog")  # Different from "dog"
        self.assertTrue(lookup(bst, "Dog"))
        self.assertTrue(lookup(bst, "dog"))  # Both should exist
        
        # Test deletion
        bst = delete(bst, "dog")
        self.assertFalse(lookup(bst, "dog"))
        self.assertTrue(lookup(bst, "cat"))  # Other strings still there
        
        # Test empty string handling
        bst = insert(bst, "")
        self.assertTrue(lookup(bst, ""))
        bst = delete(bst, "")
        self.assertFalse(lookup(bst, ""))
    
    def test_point_euclidean_distance_ordering(self):
        """Test BST with Euclidean distance from zero ordering"""
        def point_comes_before(a: Point2, b: Point2) -> bool:
            return a.distance_from_zero() < b.distance_from_zero()
        
        # Create empty BST
        bst = BinarySearchTree(point_comes_before, None)
        self.assertTrue(is_empty(bst))
        
        # Create test points with various distances
        points = [
            Point2(0, 0),      # distance = 0
            Point2(3, 4),      # distance = 5
            Point2(1, 0),      # distance = 1
            Point2(0, 2),      # distance = 2
            Point2(1, 1),      # distance = sqrt(2) ≈ 1.414
            Point2(0, 3),      # distance = 3
            Point2(2, 2),      # distance = 2*sqrt(2) ≈ 2.828
        ]
        
        # Insert points
        for point in points:
            bst = insert(bst, point)
        
        self.assertFalse(is_empty(bst))
        
        # Test lookup - all points should be found
        for point in points:
            self.assertTrue(lookup(bst, point))
        
        # Test lookup for points with distances not in the BST
        self.assertFalse(lookup(bst, Point2(10, 10)))  # distance = sqrt(200) ≈ 14.14 (not in BST)
        self.assertFalse(lookup(bst, Point2(0, 4)))    # distance = 4 (not in BST)
        
        # Test that points with same distance are handled correctly
        # Point2(3,4) and Point2(-3,-4) both have distance 5, so only first inserted should be kept
        bst_test = BinarySearchTree(point_comes_before, None)
        bst_test = insert(bst_test, Point2(3, 4))
        bst_test = insert(bst_test, Point2(-3, -4))  # Should be treated as duplicate and not inserted
        
        # Only the first one should be found (as they have equal distance)
        self.assertTrue(lookup(bst_test, Point2(3, 4)))
        # The lookup should succeed because they're considered equal by distance
        self.assertTrue(lookup(bst_test, Point2(-3, -4)))
        
        # Test deletion
        bst = delete(bst, Point2(0, 0))  # Delete origin
        self.assertFalse(lookup(bst, Point2(0, 0)))
        self.assertTrue(lookup(bst, Point2(1, 0)))  # Other points still there
        
        # Delete a point and verify it's gone
        bst = delete(bst, Point2(1, 0))  # Delete a point with unique distance
        self.assertFalse(lookup(bst, Point2(1, 0)))
        self.assertTrue(lookup(bst, Point2(0, 2)))  # Other points still there
    
    def test_edge_cases(self):
        """Test edge cases for all comparator types"""
        
        # Test with single element
        def int_comes_before(a: int, b: int) -> bool:
            return a < b
        
        bst = BinarySearchTree(int_comes_before, None)
        test_value: Value = 42
        bst = insert(bst, test_value)
        
        self.assertFalse(is_empty(bst))
        self.assertTrue(lookup(bst, test_value))
        
        # Test largest_value with single element
        largest_single: Value = largest_value(bst.tree)
        self.assertEqual(largest_single, test_value)
        
        # Delete the only element
        bst = delete(bst, test_value)
        self.assertTrue(is_empty(bst))
        self.assertFalse(lookup(bst, test_value))
    
    def test_generic_value_types(self):
        """Test BST with different Value types to ensure type safety"""
        
        # Test with float values
        def float_comes_before(a: float, b: float) -> bool:
            return a < b
        
        float_bst = BinarySearchTree(float_comes_before, None)
        float_values = [3.14, 1.5, 7.2, 2.71, 9.8]
        
        for val in float_values:
            float_bst = insert(float_bst, val)
        
        # Test largest_value returns correct type
        largest_float: Value = largest_value(float_bst.tree)
        self.assertEqual(largest_float, 9.8)
        self.assertIsInstance(largest_float, float)
        
        # Test with tuple values (comparing by first element)
        def tuple_comes_before(a: tuple, b: tuple) -> bool:
            return a[0] < b[0]
        
        tuple_bst = BinarySearchTree(tuple_comes_before, None)
        tuple_values = [(5, 'five'), (3, 'three'), (7, 'seven'), (1, 'one')]
        
        for val in tuple_values:
            tuple_bst = insert(tuple_bst, val)
        
        # Test largest_value with tuples
        largest_tuple: Value = largest_value(tuple_bst.tree)
        self.assertEqual(largest_tuple, (7, 'seven'))
        self.assertIsInstance(largest_tuple, tuple)
    
    def test_largest_value_and_delete_largest(self):
        """Test largest_value and delete_largest_value functions"""
        def int_comes_before(a: int, b: int) -> bool:
            return a < b
        
        bst = BinarySearchTree(int_comes_before, None)
        values = [5, 3, 7, 1, 9, 2, 8]
        
        for val in values:
            bst = insert(bst, val)
        
        # Test largest_value - should return the rightmost (largest) value
        largest: Value = largest_value(bst.tree)
        self.assertEqual(largest, 9)
        self.assertTrue(lookup(bst, largest))  # Largest should be in the BST
        
        # Test delete_largest_value
        new_tree = delete_largest_value(bst.tree)
        new_largest: Value = largest_value(new_tree)
        self.assertEqual(new_largest, 8)  # 9 removed, 8 is now largest
        self.assertFalse(lookup(BinarySearchTree(int_comes_before, new_tree), 9))  # 9 should be gone
        
        # Test with single node
        single_node = Node(100, None, None)
        single_largest: Value = largest_value(single_node)
        self.assertEqual(single_largest, 100)
        result = delete_largest_value(single_node)
        self.assertIsNone(result)  # Should return None after removing only node
    
    def test_delete_root_function(self):
        """Test delete_root function specifically"""
        def int_comes_before(a: int, b: int) -> bool:
            return a < b
        
        # Create a tree manually for precise testing
        # Tree structure:     5
        #                   /   \
        #                  3     7
        #                 / \   / \
        #                1   4 6   9
        left_subtree = Node(3, Node(1, None, None), Node(4, None, None))
        right_subtree = Node(7, Node(6, None, None), Node(9, None, None))
        root = Node(5, left_subtree, right_subtree)
        
        # Delete root - should promote largest from left subtree (4)
        new_root = delete_root(root)
        self.assertIsNotNone(new_root)
        assert new_root is not None  # Type narrowing for mypy
        
        # The new root should be the largest value from the left subtree
        expected_new_root: Value = 4
        self.assertEqual(new_root.value, expected_new_root)
        
        # Verify other values are still accessible
        new_bst = BinarySearchTree(int_comes_before, new_root)
        self.assertTrue(lookup(new_bst, 1))  # Other values still there
        self.assertTrue(lookup(new_bst, 3))
        self.assertFalse(lookup(new_bst, 5))  # Original root should be gone
        
        # Test delete_root with no left subtree
        right_only = Node(5, None, Node(7, None, None))
        result = delete_root(right_only)
        self.assertIsNotNone(result)
        assert result is not None  # Type narrowing for mypy
        expected_value: Value = 7
        self.assertEqual(result.value, expected_value)  # Should return right subtree
        
        # Test delete_root with no right subtree  
        left_only = Node(5, Node(3, None, None), None)
        result = delete_root(left_only)
        self.assertIsNotNone(result)
        assert result is not None  # Type narrowing for mypy
        expected_left_value: Value = 3
        self.assertEqual(result.value, expected_left_value)  # Should return left subtree

if (__name__ == '__main__'):
    unittest.main()