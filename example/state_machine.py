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

    @staticmethod
    def lookup_equation(reference_to_self, label):
        for item in reference_to_self.declaration_list:
            if item.label == label:
                return item
        return None

    @staticmethod
    def local_lookup_equation(reference_to_self, label):
        if label == reference_to_self.label:
            return reference_to_label
        else:
            return None

    def __init__(self):
        # Declare attributes

        syn(Transition, "source_attribute", lambda n : n.source)
        syn(Transition, "target_attribute", lambda n : n.target)

        inh(Declaration, "lookup")

        eq(StateMachine, "lookup", lambda n, label : MinTree.lookup_equation(n, label))

        #syn(State, "localLookup", lambda n: None)

        eq(State, "localLookup", lambda n, label : MinTree.local_lookup_equation(n, label))


#################################################
# Tree Specification
#################################################


class StateMachine:

    def __init__(self):
        self.declaration_list = []

    def add_declaration(self, decl):
        setattr(self, decl.label, decl)
        self.declaration_list.append(getattr(self, decl.label))


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

    def get_children(self):
        return self.declaration_list

class Declaration(ABC):

    def __init__(self):
        super().__init__()


class State(Declaration):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def get_children(self):
        return []


class Transition(Declaration):
    def __init__(self, label, source, target):
        super().__init__()
        self.label = label
        self.source = source
        self.target = target

    def get_children(self):
        return []


#################################################
# Driver Code
#################################################


class MinTreeExample:

    def __init__(self):

        Weaver(MinTree)  # Just give the reference to the RAG class

        self.m = StateMachine()
        self.m.add_declaration(State("S1"))
        self.m.add_declaration(State("S2"))
        self.m.add_declaration(State("S3"))

        self.m.add_declaration(Transition("a", "S1", "S2"))
        self.m.add_declaration(Transition("b", "S2", "S1"))
        self.m.add_declaration(Transition("a", "S2", "S3"))

        Weaver.infer_parents(self.m) #Infer parents for the tree

def run_example():
    a = MinTreeExample()

    machine = a.m

    for item in a.m.declaration_list:
        if isinstance(item, State):
            pass
            #print(item.label)
        else:
            print(str(item.source_attribute()), end = '')
            print(" - > ", end = '')
            print(str(item.target_attribute()))
            print("Doing some lookup")
            print(item.lookup("S1"))
            print(item.lookup("S2"))
            print(item.lookup("S3"))
            print(item.lookup("S4"))
