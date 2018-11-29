from unittest import TestCase

from src.library import inh, eq, Weaver


#################################################
# Grammar Specification
#################################################


class RAG:

    def __init__(self):
        # Declare attributes

        inh(Node, 'root')

        eq(Root, 'root', lambda n: n)


#################################################
# Tree Specification
#################################################


class Root:
    def __init__(self):
        self.node = None

    def set_node(self, node):
        self.node = node

    def get_children(self):
        if self.node is None:
            return []
        else:
            return [self.node]


class Node:
    def __init__(self):
        self.node = None

    def set_node(self, node):
        self.node = node

    def get_children(self):
        if self.node is None:
            return []
        else:
            return [self.node]


#################################################
# Test Classes
#################################################


class TestClass(TestCase):

    def setUp(self):
        Weaver(RAG)

        self.root = Root()
        self.root.set_node(Node())
        self.root.node.set_node(Node())

        Weaver.infer_parents(self.root)

        self.root.node.node.root()

        print(self.root.node.node.root())
        print(self.root)

    def test_basic_inheritance1(self):
        self.assertEqual(self.root.node.node.root(), self.root)
