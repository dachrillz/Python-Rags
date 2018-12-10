"""
The files in this folder tests so that the library can be modularized.
That is, can the RAG be defined in multiple files.

This file defines the inherited attributes
"""

from src.library import inh, eq

from tests.modularization.tree_definition import Node, Program


#################################################
# Grammar Specification
#################################################

class MinTreeSecond:
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
        eq(Program, 'globalmin', lambda n: 42)

