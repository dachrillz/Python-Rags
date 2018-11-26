from unittest import TestCase

from abc import ABC

from library import inh, eq, syn, Weaver

#################################################
# Grammar Specification
#################################################


class RAG:

    def __init__(self):
        # Declare attributes

        inh(Node, "inhAttr")

        eq(Root, "inhAttr", lambda n: -1, 'Node')
        eq(Root, "inhAttr", lambda n: 0, 'Child')


#################################################
# Tree Specification
#################################################


class Root:
    def __init__(self):
        self.node = None

    def set_node(self, node):
        self.node = node

    @staticmethod
    def get_parent_class():
        return []


class Node:
    def __init__(self):
        self.node = None

    def set_node(self, node):
        self.node = node

    @staticmethod
    def get_parent_class():
        return [Root, Node]

#################################################
# Test Classes
#################################################


class TestClass(TestCase):

    def setUp(self):
        weaver = Weaver(RAG)
        weaver.traverse_and_inject()

        self.root = Root()
        self.root.set_node(Node())
        self.root.node.set_node(Node())

    def test_basic_inheritance1(self):
        self.assertEqual(self.root.node.node.inhAttr(), 0)

    def test_basic_inheritance2(self):
        self.assertEqual(self.root.node.inhAttr(), -1)
