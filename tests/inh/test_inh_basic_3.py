from unittest import TestCase

from abc import ABC

from library import inh, eq, syn, Weaver

#################################################
# Grammar Specification
#################################################


class RAG:

    def __init__(self):
        # Declare attributes

        inh(A, 'value')

        eq(Node, 'value', lambda n: 77, 'Left')
        eq(Node, 'value', lambda n: -1, 'Right')


#################################################
# Tree Specification
#################################################


class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @staticmethod
    def get_parent_class():
        return []


class A:
    def __init__(self):
        self.node = None

    @staticmethod
    def get_parent_class():
        return [Node]


class Left(A):
    def __init__(self):
        super().__init__()


class Right(A):
    def __init__(self):
        super().__init__()

#################################################
# Test Classes
#################################################


class TestClass(TestCase):

    def setUp(self):
        weaver = Weaver(RAG)
        weaver.traverse_and_inject()

        left = Left()
        right = Right()

        self.node = Node(left, right)

    def test_basic_inheritance1(self):
        self.assertEqual(77, self.node.left.value())
        self.assertEqual(-1, self.node.right.value())

