from abc import ABC

from src.library import inh, eq, syn, Weaver


#################################################
# Grammar Specification
#################################################


class MinTree:
    """
    This is a class that defines the attributes we want to give to the a tree.

    That is, this is the class where one defines the reference attribute grammar.
    This is also the class we expect the user to define!

    The user of this package Declares attributes, and then Defines equations for these attributes.
    """

    def __init__(self):
        # Declare attributes

        # Global min attribute
        inh(Node, "globalmin")

        # First Argument is the node that is to contain the equation
        eq(Program, 'globalmin', lambda x: 42, 'Node')

        # Local min attributes
        syn(Program, "localmin")
        syn(Leaf, "localmin")
        syn(Pair, "localmin")

        # Define their equations
        eq(Leaf, 'localmin', lambda x: x.value)
        eq(Pair, 'localmin', lambda x: min(x.left.localmin(), x.right.localmin()))
        eq(Program, 'localmin', lambda x: 0)


#################################################
# Tree Specification
#################################################

#  This part of the code specifies a Python Tree that we want to attribute


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


class Node(ABC):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_parent_class():
        return [Pair, Program]


class Pair(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

    @staticmethod
    def get_parent_class():
        return [Pair, Program]


class Leaf(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_children(self):
        return []

    @staticmethod
    def get_parent_class():
        return [Pair]


#################################################
# Driver Code
#################################################


class MinTreeExample:

    def __init__(self):
        weaver = Weaver(MinTree)  # Just give the reference to the RAG class
        instance = Program(Pair(Leaf(1), Pair(Leaf(2), Leaf(3))))

        # simply get all the nodes in tree after attribution, so one can get the nodes to check the result.
        self.allnodes = instance.traverse()

        # Instance of the weaver class
        weaver.traverse_and_inject()

    def print_global_min(self):

        for item in self.allnodes:
            if not isinstance(item, Program):
                print(item)
                print(item.globalmin())

    def print_local_min(self):
        for i in range(len(self.allnodes)):
            print(self.allnodes[i].localmin())


if __name__ == '__main__':
    a = MinTreeExample()

    print("Printing the global mins")
    a.print_global_min()

    print("Printing the local mins")
    a.print_local_min()
