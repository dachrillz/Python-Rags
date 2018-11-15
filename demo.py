########################################################
#
# LIBRARY STUFF!
#
########################################################


class SynAttr():
    '''
    This class is the Synthesized Attribute Class.

    - Type of Class is the class node that is to be attributed.
    - Attribute name is the name of the attribute

    - self.name is the name of the attribute that is to be given an equation
    - the expression is an expression that we are to implement.
    '''
    def __init__(self, type_of_class, attribute_name):
        self.type_of_class = type_of_class
        self.attribute_name = attribute_name

    def equation(self, name, attribute):
        self.name = name
        self.attribute = attribute

class InhAttr():
    def __init__(self, type_of_class, attribute_name):
        self.type_of_class = type_of_class
        self.attribute_name = attribute_name

class InhEq():
    def __init__(self, class_type, name, attribute):
        self.class_type = class_type
        self.name = name
        self.attribute = attribute
        setattr(class_type, name, attribute)


class Weaver:
    """
    This is the class that weaves together the attribute grammar with a tree.
    """

    def __init__(self, attribute_class):
        self.attribute_class = attribute_class() #An instance of the user defined attribute class

        #Get all declared self variables from the attribute class and add them to a list so that we can iterate over them
        self.synthesized_list_of_attribute_declarations = [] #@TODO which data structure should I be?
        self.inherited_list_of_attribute_declarations = [] #@TODO which data structure should I be?
        for _, value in vars(self.attribute_class).items():
            if isinstance(value,SynAttr):
                self.synthesized_list_of_attribute_declarations.append(value)
            elif isinstance(value,InhAttr):
                self.inherited_list_of_attribute_declarations.append(value)

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
        This function traverses all Attribute Declarations and injects them into the tree.
        """

        #Synthesized attributes
        for attribute_declaration in self.synthesized_list_of_attribute_declarations:

            class_reference = attribute_declaration.type_of_class #Get a reference to the class that is to be attributed
            name_of_attribute = attribute_declaration.attribute_name #Get attribute name
            function_to_be_injected = attribute_declaration.attribute #Get the attribute

            self.inject(class_reference, name_of_attribute, function_to_be_injected) #inject the attribute into the tree.

        #Inherited attributes
        for attribute_declaration in self.inherited_list_of_attribute_declarations:

            class_reference = attribute_declaration.type_of_class
            name_of_attribute = attribute_declaration.attribute_name

            attribute = self.traverse_upwards_tree_for_inh_equation(class_reference, name_of_attribute, class_reference.get_parent_class())

            print(attribute)

            self.inject(class_reference, name_of_attribute, attribute)



    def inject(self, node, name_of_attribute, attribute):
        #1st arg is a class
        #2nd arg is name of attribute
        #3rd arg is the attribute to be set
        setattr(node, name_of_attribute, attribute)

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

        #Declare attributes

        #Global min attribute
        self.globalMinLeaf = InhAttr(Leaf, "globalmin")
        self.globalMinPair = InhAttr(Pair, "globalmin")

        #First Argument is the node that
        self.globalMin     = InhEq(Program, 'globalmin', lambda x : 42)

        #Local min attributes
        self.program = SynAttr(Program, "localmin")
        self.leaf = SynAttr(Leaf, "localmin")
        self.pair = SynAttr(Pair, "localmin")

        #Define their equations
        self.leaf.equation('localmin', lambda x : x.value)
        self.pair.equation('localmin', lambda x : min(x.left.localmin() , x.right.localmin()))
        self.program.equation('localmin', lambda x : 0)

#########################################################
#
# Example implementation of a tree class in Python
#
##########################################################

#The abstract class construct has to be imported in Python
from abc import ABC

class Program:

    def __init__(self, node):
        self.node = node

    def traverse_tree_aux(self, node, result):
        '''
        Support Function for the tree traversal
        '''

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
        result = [self] #The result is currently stored as a list, should this be a generator? Also how to enforce such that a tree actually behaves nicely.

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

    #Instance of the weaver class
    weaver = Weaver(MinTree) #Just give the reference to the RAG class
    weaver.traverse_and_inject()

    #an instance of this class
    instance = Program(Pair(Leaf(1), Pair(Leaf(2), Leaf(3))))

    allnodes = instance.traverse() #this simply gets all the nodes in the tree after the tree has been attributed, so one can print the nodes to check the result.

    print(allnodes)

    #print(allnodes[0].globalmin())

    for item in allnodes:
        print(str(item), item.localmin())

    for item in allnodes:
        print(str(item), item.globalmin())
