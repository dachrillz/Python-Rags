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


def syn(type_of_class, attribute_name, equation=None):
    if equation is None:
        setattr(type_of_class, attribute_name, None)
    else:
        setattr(type_of_class, attribute_name, equation)


def inh(type_of_class, attribute_name):
    AttributeContainer.inherited_dictionary[str(type_of_class)] = (type_of_class, attribute_name)


def eq(type_of_class, attribute_name, equation, child=None):
    if child is None:
        setattr(type_of_class, attribute_name, equation)
    else:
        # if the equation gives a child, we know that this is an equation that is to be inherited
        if hasattr(type_of_class, "equation_container"):
            type_of_class.equation_container[child] = (attribute_name, equation)
        else:
            equation_container = dict()
            equation_container[child] = (attribute_name, equation)
            setattr(type_of_class, "equation_container", equation_container)


class InhAttr:
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

    @staticmethod
    def traverse_upwards_tree_for_inh_equation(reference_to_child, name_of_attribute, next_parent):

        visited = set()

        def traversal_closure(ref, name, next_par):
            for current_parent in next_par:

                if hasattr(current_parent, 'equation_container'):
                    if reference_to_child.__name__ in vars(current_parent)['equation_container']:
                        if name_of_attribute == vars(current_parent)['equation_container'][reference_to_child.__name__][
                            0]:
                            return vars(current_parent)['equation_container'][reference_to_child.__name__][1]

                    elif 'Child' in vars(current_parent)['equation_container']:
                        if name_of_attribute == vars(current_parent)['equation_container']['Child'][0]:
                            return vars(current_parent)['equation_container']['Child'][1]

                elif current_parent not in visited:
                    visited.add(current_parent)
                    current_par = current_parent.get_parent_class()
                    attr = traversal_closure(ref, name, current_par)
                    return attr

        return traversal_closure(reference_to_child, name_of_attribute, next_parent)

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

    def traverse_and_inject(self):
        """
        This function traverses all Inherited Declarations, searches for a defined equation
        and then injects them into the tree.
        """

        for _, attribute_declaration in self.inherited_dict_of_attribute_declarations.items():
            class_reference = attribute_declaration[0]
            name_of_attribute = attribute_declaration[1]

            attribute = self.traverse_upwards_tree_for_inh_equation(class_reference, name_of_attribute,
                                                                    class_reference.get_parent_class())

            setattr(class_reference, name_of_attribute, attribute)

            # This gets all classes that inherit from a certain class
            # This is used to attribute Left and Right, when Left:A Right:A
            all_child_classes = Weaver.inheritors(class_reference)

            for class_reference in all_child_classes:

                attribute = self.traverse_upwards_tree_for_inh_equation(class_reference, name_of_attribute,
                                                                        class_reference.get_parent_class())

                setattr(class_reference, name_of_attribute, attribute)
