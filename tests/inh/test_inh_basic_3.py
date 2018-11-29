from unittest import TestCase

from src.library import inh, eq, Weaver


#################################################
# Grammar Specification
#################################################


class RAG:

    def __init__(self):
        # Declare attributes

        inh(A, 'value')

        eq(Node, 'value', lambda n: 77)
        eq(Node, 'value', lambda n: -1)


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

    def get_children(self):
        return [self.left, self.right]


class A:
    def __init__(self):
        self.node = None

    def get_children(self):
        if self.node is None:
            return []
        else:
            return [self.node]


class Left(A):
    def __init__(self):
        super().__init__()

    def get_children(self):
        return []


class Right(A):
    def __init__(self):
        super().__init__()

    def get_children(self):
        return []


#################################################
# Test Classes
#################################################


class TestClass(TestCase):

    def setUp(self):
        weaver = Weaver(RAG)

        left = Left()
        right = Right()

        self.node = Node(left, right)

        Weaver.infer_parents(self.node)

    def test_basic_inheritance1(self):
        self.assertEqual(-1, self.node.left.value())
        self.assertEqual(-1, self.node.right.value())
