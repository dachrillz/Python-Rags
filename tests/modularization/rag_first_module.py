"""
The files in this folder tests so that the library can be modularized.
That is, can the RAG be defined in multiple files.

This file defines the circular attributes
"""

from src.library import eq, syn

#################################################
# Grammar Specification
#################################################
from tests.modularization.tree_definition import Program, Leaf, Pair


class MinTreeFirst:
    """
    This is a class that defines the attributes we want to give to the a tree.

    That is, this is the class where one defines the reference attribute grammar.
    This is also the class we expect the user to define!

    The user of this package Declares attributes, and then Defines equations for these attributes.
    """

    def __init__(self):
        # Declare attributes

        # Local min attributes
        syn(Program, "localmin")
        syn(Leaf, "localmin")
        syn(Pair, "localmin")

        # Define their equations
        eq(Leaf, 'localmin', lambda x: x.value)
        eq(Pair, 'localmin', lambda x: min(x.left.localmin(), x.right.localmin()))
        eq(Program, 'localmin', lambda x: 0)
