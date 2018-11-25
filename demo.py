########################################################
#
# LIBRARY STUFF!
#
########################################################

class AttributeContainer:
    """
    This class simply contains a list that statically
    contains a reference to all the defined attributes
    by the user
    """

    inherited_dictionary = {}


def syn(type_of_class, attribute_name, equation = None):

    if equation is None:
        setattr(type_of_class, attribute_name, None)
    else:
        setattr(type_of_class, attribute_name, equation)


def inh(type_of_class, attribute_name):

    AttributeContainer.inherited_dictionary[str(type_of_class)] = (type_of_class, attribute_name)


def eq(type_of_class, attribute_name, equation):

    setattr(type_of_class, attribute_name, equation)


class InhAttr():
    def __init__(self, type_of_class, attribute_name):
        self.type_of_class = type_of_class
        self.attribute_name = attribute_name


class Weaver:
    """
    This is the class that weaves together the attribute grammar with a tree.
    """

    def __init__(self, attribute_class):
        self.attribute_class = attribute_class()  # An instance of the user defined attribute class

        # Get declared self variables from the attribute class and add them to a list so that we can iterate over them
        self.inherited_dict_of_attribute_declarations = AttributeContainer.inherited_dictionary

    def traverse_upwards_tree_for_inh_equation(self, reference_to_child, name_of_attribute, next_parent):

        visited = set()

        def traversal_closure(reference_to_child, name_of_attribute, next_parent):

            for current_parent in next_parent:
                if name_of_attribute in vars(current_parent):
                    return vars(current_parent)[name_of_attribute]

                elif current_parent not in visited:
                    visited.add(current_parent)
                    ref = reference_to_child
                    name = name_of_attribute
                    current_par = current_parent.get_parent_class()
                    function = traversal_closure(ref, name, current_par)
                    return function

        return traversal_closure(reference_to_child, name_of_attribute, next_parent)


    def traverse_and_inject(self):
        """
        This function traverses all Inherited Declarations, searches for a defined equation
        and then injects them into the tree.
        """

        for _, attribute_declaration in self.inherited_dict_of_attribute_declarations.items():

            class_reference = attribute_declaration[0]
            name_of_attribute = attribute_declaration[1]

            attribute = self.traverse_upwards_tree_for_inh_equation(class_reference, name_of_attribute, class_reference.get_parent_class())


            setattr(class_reference, name_of_attribute, attribute)



########################################################
#
# USER STUFF!
#
########################################################

#########################################################
#
# The RAG specification
#
##########################################################



class MinTree():
    """
    This is a class that defines the attributes we want to give to the a tree.

    That is, this is the class where one defines the reference attribute grammar.
    This is also the class we expect the user to define!

    The user of this package Declares attributes, and then Defines equations for these attributes.
    """

    def __init__(self):

        # Declare attributes

        # Global min attribute
        inh(Leaf, "globalmin")
        inh(Pair, "globalmin")

        # First Argument is the node that
        eq(Program, 'globalmin', lambda x: 42)

        # Local min attributes
        syn(Program, "localmin")
        syn(Leaf, "localmin")
        syn(Pair, "localmin")

        # Define their equations
        eq(Leaf, 'localmin', lambda x: x.value)
        eq(Pair, 'localmin', lambda x: min(x.left.localmin(), x.right.localmin()))
        eq(Program, 'localmin', lambda x: 0)

#########################################################
#
# Example implementation of a tree class in Python
#
##########################################################

# The abstract class construct has to be imported in Python
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
        result = [self] # The result is currently stored as a list, should this be a generator? Also how to enforce such that a tree actually behaves nicely.

        first_node = self.node

        self.traverse_tree_aux(first_node, result)

        return result



class Node(ABC):

    def __init__(self):
        super().__init__()

    def get_parent_class():
        return [Pair, Program]

class Pair(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

    def get_parent_class():
        return [Pair, Program]

class Leaf(Node):
    def __init__(self, value):
        self.value = value

    def get_children(self):
        return []

    def get_parent_class():
        return [Pair]

#########################################################
#
# MAIN AND DRIVER CODE!
#
##########################################################

if __name__ == '__main__':

    # Instance of the weaver class
    weaver = Weaver(MinTree) #Just give the reference to the RAG class
    weaver.traverse_and_inject()

    # an instance of this class
    instance = Program(Pair(Leaf(1), Pair(Leaf(2), Leaf(3))))

    allnodes = instance.traverse()  # this simply gets all the nodes in the tree after the tree has been attributed, so one can print the nodes to check the result.

    print(allnodes)

    # print(allnodes[0].globalmin())

    for item in allnodes:
        print(str(item), item.localmin())

    for item in allnodes:
        print(str(item), item.globalmin())
