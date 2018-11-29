from unittest import TestCase

from abc import ABC

from src.library import Weaver


#################################################
# Tree Specification
#################################################


class Program:

    def __init__(self, value, node):
        self.value = value
        self.node = node

    def get_children(self):
        return [self.node]

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


class Node(ABC):

    def __init__(self):
        super().__init__()


class Pair(Node):
    def __init__(self, value, left, right):
        super().__init__()
        self.value = value
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

    def get_children(self):
        return []


#################################################
# Test Classes
#################################################

class RAG:
    pass


class MinTreeTest(TestCase):

    def setUp(self):
        self.weaver = Weaver(RAG)  # Just give the reference to the RAG class
        self.instance = Program(0, Pair(1, Leaf(2), Pair(3, Leaf(4), Leaf(5))))

    def test_infer_parents(self):
        self.weaver.infer_parents(self.instance)

        pair1 = self.instance.get_children()[0]

        self.assertEqual(pair1.get_parent(), self.instance)

        leaf2 = pair1.get_children()[0]
        pair3 = pair1.get_children()[1]

        self.assertEqual(leaf2.get_parent(), pair1)
        self.assertEqual(pair3.get_parent(), pair1)

        leaf4 = pair3.get_children()[0]
        leaf5 = pair3.get_children()[1]

        self.assertEqual(leaf4.get_parent(), pair3)
        self.assertEqual(leaf5.get_parent(), pair3)
