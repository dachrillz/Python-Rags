from unittest import TestCase

from abc import ABC

from src.library import inh, eq, syn, Weaver


#################################################
# Grammar Specification
#################################################

class Calc:
    """
    This is a class that defines the attributes we want to give to the a tree.

    That is, this is the class where one defines the reference attribute grammar.
    This is also the class we expect the user to define!

    The user of this package Declares attributes, and then Defines equations for these attributes.
    """

    def __init__(self):
        # Declare attributes

        # Final computation
        inh(Expr, "finalCalc")

        # First Argument is the node that is to contain the equation
        eq(Program, 'finalCalc', lambda n: n.node.localCalc())

        # Local computation
        syn(Mul, "localCalc")
        syn(Add, "localCalc")
        syn(Div, "localCalc")
        syn(Sub, "localCalc")
        syn(Numeral, "localCalc")

        # Define their equations
        eq(Mul, 'localCalc', lambda x: x.left.localCalc()* x.right.localCalc())
        eq(Add, 'localCalc', lambda x: x.left.localCalc()+ x.right.localCalc())
        eq(Div, 'localCalc', lambda x: x.left.localCalc()/ x.right.localCalc())
        eq(Sub, 'localCalc', lambda x: x.left.localCalc()- x.right.localCalc())
        eq(Numeral, 'localCalc', lambda x: x.value)

#################################################
# Tree Specification
#################################################


class Program:

    def __init__(self, node):
        self.node = node

    def traverse_tree_aux(self, node, result):
        """
        Support Function for the tree traversal
        """

        result.append(node)

        if isinstance(node.left, Expr):
            result.append(node.left)
        else:
            self.traverse_tre_aux(node.left, result)

        if isinstance(node.right, Expr):
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


class Expr(ABC):

    def __init__(self):
        super().__init__()

class Mul(Expr):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

class Sub(Expr):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

class Add(Expr):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

class Div(Expr):

    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

class Numeral(Expr):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_children(self):
        return []


#################################################
# Test Classes
#################################################


class CalcTest(TestCase):

    def setUp(self):
        Weaver(Calc)  # Just give the reference to the RAG class
        self.instance = Program(Mul(Add(Numeral(1), Numeral(3)), Numeral(2)))

        Weaver.infer_parents(self.instance)

        # simply get all the nodes in tree after attribution, so one can get the nodes to check the result.
        self.allnodes = self.instance.traverse()

    def test_finalCalc(self):
        self.assertEqual(self.instance.node.finalCalc(),8)

    def test_localCalc(self):
        self.assertEqual(self.instance.node.localCalc(), 8)

        self.assertEqual(self.instance.node.left.localCalc(), 4)

        self.assertEqual(self.instance.node.left.left.localCalc(), 1)

        self.assertEqual(self.instance.node.left.right.localCalc(), 3)

        self.assertEqual(self.instance.node.right.localCalc(), 2)



