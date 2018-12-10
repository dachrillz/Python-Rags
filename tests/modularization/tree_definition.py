"""
The files in this folder tests so that the library can be modularized.
That is, can the RAG be defined in multiple files.

This file defines the tree that is to be attributed.

It has to be defined in a separate file in order to avoid circular imports.
"""
from abc import ABC


class Program:

    def __init__(self, node):
        self.node = node

    def traverse_tree_aux(self, node, result):
        """
        Support Function for the tree traversal
        """

        result.append(node)

        if isinstance(node.left, Leaf):
            result.append(node.left)
        else:
            self.traverse_tre_aux(node.left, result)

        if isinstance(node.right, Leaf):
            result.append(node.right)
        else:
            self.traverse_tree_aux(node.right, result)

    def traverse(self):
        """
        In order traversal of the tree.

        Returns all the nodes in a list.
        """
        result = [self]

        first_node = self.node

        self.traverse_tree_aux(first_node, result)

        return result

    def get_children(self):
        return [self.node]


class Node(ABC):

    def __init__(self):
        super().__init__()


class Pair(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]


class Leaf(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_children(self):
        return []
