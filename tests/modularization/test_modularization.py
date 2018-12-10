"""
The files in this folder tests so that the library can be modularized.
That is, can the RAG be defined in multiple files.

This is the main file that binds all the other files together.
"""

from unittest import TestCase

from src.library import Weaver

from tests.modularization.rag_first_module import MinTreeFirst
from tests.modularization.rag_second_module import MinTreeSecond

from tests.modularization.tree_definition import Program, Pair, Leaf


#################################################
# Test Classes
#################################################


class MinTreeTest(TestCase):

    def setUp(self):
        Weaver(MinTreeFirst)  # Just give the reference to the RAG class
        Weaver(MinTreeSecond)
        instance = Program(Pair(Leaf(1), Pair(Leaf(2), Leaf(3))))

        Weaver.infer_parents(instance)

        # simply get all the nodes in tree after attribution, so one can get the nodes to check the result.
        self.allnodes = instance.traverse()

    def test_global_min(self):

        for item in self.allnodes:
            if not isinstance(item, Program):
                self.assertEqual(item.globalmin(), 42)

    def test_local_min(self):

        for i in range(len(self.allnodes)):

            if i is 0:
                self.assertEqual(0, self.allnodes[i].localmin())
            elif i is 1:
                self.assertEqual(1, self.allnodes[i].localmin())
            elif i is 2:
                self.assertEqual(1, self.allnodes[i].localmin())
            elif i is 3:
                self.assertEqual(2, self.allnodes[i].localmin())
            elif i is 4:
                self.assertEqual(2, self.allnodes[i].localmin())
            elif i is 5:
                self.assertEqual(3, self.allnodes[i].localmin())
