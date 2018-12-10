########################################################
#
# LIBRARY STUFF!
#
########################################################
from functools import lru_cache


def syn(type_of_class, attribute_name, equation=None):
    """
    @TODO: this is somewhat inconsistent when one gives the equation directly, rewrite that part
    :param type_of_class:
    :param attribute_name:
    :param equation:
    :return:
    """

    @lru_cache(maxsize=None)
    def lookup_function(self):
        closure_name = '__eq__' + attribute_name

        if hasattr(self.__class__, closure_name):
            return getattr(self.__class__, closure_name)(self)
        else:
            return getattr(type_of_class, closure_name)(self)

    if equation is None:
        setattr(type_of_class, attribute_name, lookup_function)
    else:
        setattr(type_of_class, attribute_name, equation)


def inh(type_of_class, attribute_name):
    # We use closures to be able to pass the attribute_name into the function later

    @lru_cache(maxsize=None)
    def get_function_from_parent(self, *args):
        closure_attribute = "__eq__" + attribute_name
        parent = self.get_parent()
        if parent is not None:
            if hasattr(parent, "defines") and parent.defines(closure_attribute):
                attribute = getattr(parent, closure_attribute)
                return attribute(*args)
            else:
                return get_function_from_parent(parent)

    setattr(type_of_class, attribute_name, get_function_from_parent)


def eq(type_of_class, attribute_name, equation):
    attribute_name = '__eq__' + attribute_name

    #If the parent class defins
    if hasattr(type_of_class.__bases__[0], attribute_name):
        syn(type_of_class, attribute_name)
        setattr(type_of_class, attribute_name, equation)
    else:
        setattr(type_of_class, attribute_name, equation)

        setattr(type_of_class, "defines", lambda self, n: hasattr(self, n))


class Weaver:
    """
    This is the class that weaves together the attribute grammar with a tree.
    """

    def __init__(self, attribute_class):
        self.attribute_class = attribute_class()  # An instance of the user defined attribute class

        # Get declared self variables from the attribute class and add them to a list so that we can iterate over them

    @staticmethod
    def inheritors(class_):
        subclasses = set()
        work = [class_]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return subclasses

    @staticmethod
    def infer_parents(root_of_tree):
        """
        Assumes that each node has a function called get_children,
        which returns a list of each child

        :param root_of_tree:
        :return:
        """

        setattr(root_of_tree, "get_parent", lambda: None)

        def inorder_traversal(node):
            children = node.get_children()
            if len(children) is not 0:
                for child in children:
                    setattr(child, "get_parent", lambda: node)
                    inorder_traversal(child)

        inorder_traversal(root_of_tree)
