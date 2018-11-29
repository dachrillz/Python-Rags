from unittest import TestCase

from src.library import inh, eq, Weaver


#################################################
# Grammar Specification
#################################################


class RAG:

    def __init__(self):
        # Declare attributes

        inh(Node, "inhAttr")

        eq(Root, "inhAttr", lambda n: -1)
        eq(Node, "inhAttr", lambda n: 0)


#################################################
# Tree Specification
#################################################


class Root:
    def __init__(self):
        self.node = None

    def set_node(self, node):
        self.node = node

    def get_children(self):
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
    """
    Test inspiration: https://bitbucket.org/jastadd/jastadd-test/src/master/tests/inh/basic_01p/
    """

    def setUp(self):
        weaver = Weaver(RAG)

        self.root = Root()
        self.root.set_node(Node())
        self.root.node.set_node(Node())

        Weaver.infer_parents(self.root)

        self.root.node.node.inhAttr()

    def test_basic_inheritance1(self):
        self.assertEqual(self.root.node.node.inhAttr(), 0)

    def test_basic_inheritance2(self):
        self.assertEqual(self.root.node.inhAttr(), -1)
