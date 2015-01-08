##############################################################################
# Jason Maynard
# U30503758
# Assignment 5
##############################################################################
# These are the classes and methods used in the project.  This file
# is called by the main program to perform the calculations.
#
# References: 
# My AI group - Nataliya Ivanova, Josh Philpott. 
# The supporting website for the book found at http://aima.cs.berkeley.edu
# http://www.cs.bham.ac.uk/internal/courses/intro-ai/current/notes.php
# 
##############################################################################

import math
import copy  # https://docs.python.org/2/library/copy.html

# ----------------------------------------------------------------------------
class aLeaf:
    """Leaf node used to indicate a pure set or decision in the tree."""
# ----------------------------------------------------------------------------

    def __init__(self, value):
        self.value = value
        
    def is_leaf(self):
        return True


# ----------------------------------------------------------------------------
class aNode:
    """The main node class used to build the tree."""
# ----------------------------------------------------------------------------
    
    def __init__(self, attribute):
        self.children = {}
        self.split_name = attribute
        
    def set_children(self, children):
        self.children = children
        
    def is_leaf(self):
        return False
        
        
# ----------------------------------------------------------------------------
class aTree:
    """The overall decision tree."""
# ----------------------------------------------------------------------------
    def __init__(self):
        self._tree = None
        self._is_trained = False


    def entropy(self, examples):
        """Finds the entropy in a set of examples.  Uses a temporary
        table to store the values for computation."""
        
        tmp_table = {}      # A place to count the target values
        total = 0.0         # Total count
        entropy = 0.0       # Initialize entropy to zero
        
        for e in examples:
            total += 1      # Increment the total each time in the loop
            
            # If the value is in the table, increment it
            if e[0] in tmp_table:
                tmp_table[e[0]] += 1
            
            # Otherwise, add it to the table
            else:
                tmp_table[e[0]] = 1.0
        
        # Iterate through the table to sum the total entropy
        # print "\nCalculating entropy... "
        for k, v in tmp_table.iteritems():
            entropy -= ((v / total) * math.log((v /total), 2))
        
        # print "The entropy is: ", entropy
        return entropy
    
    def gain(entropy, remainder_list):
        """Returns the gain calculated by taking the starting entropy
        and subtracting the variables remainder passed as a list.
    
        Parameter: entropy is the starting entropy
        Parameter: remainder_list is the set of values used to calculate the
        remainder.
        
        Example gain(.95, [(.5, 0), (.5, .81)]) = .545
        
        Note: Make sure to enter any fractions : one of the values is a
        float to avoid intiger division!
        """
        
        # Initialize gain to be the starting entropy then subtract entropy
        # according to the values in the remainder list.
        gain = entropy
        
        for item in remainder_list:
            gain -= item[0] * item[1]
        
        return gain
    
    
    def split_by(self, examples, attribute):
        """Returns a list for each value of attribute"""

        subsets = []
        names = []
        
        for line in examples:
            if line[attribute] in names:
                i = names.index(line[attribute])
                subsets[i].append(line)
            else:
                names.append(line[attribute])
                subsets.append([line])
        return subsets
    
    def get_children(self, examples, attribute):
        """Returns a dictionary of children nodes."""
        
        children = {}
        
        for line in examples:
            if line[attribute] in children:
                i = line.pop(attribute)
                children[i].append(line)
            else:
                i = line.pop(attribute)
                children[i] = [line]
                
        return children
    
    
    def choose_attribute(self, examples):
        """Returns the best attribute to split on based on information
        gain.  Starts wiht total entropy at the top level then for
        each split to make decision."""
        
        # First get the top level entropy
        entropy_top = self.entropy(examples)
        
        # Initialize attribute and gain. Set gain to smallest possible
        # starting value. 
        attribute = 0
        gain = 0
        
        # Get the entropy values after various splits
        for line in range(1, len(examples[0])):
            example_sets = self.split_by(examples, line)
            temp_gain = entropy_top
            
            for set in example_sets:
                temp_entropy = (float(len(set)) / len(examples)) * \
                    self.entropy(set)
                temp_gain -= temp_entropy
                
            if temp_gain >= gain:
                attribute = line
                gain = temp_gain
        
        return attribute
    
    
    def decision_tree_learning(self, examples, attributes,
                               parent_examples=None):
        """Recursively creates a decision tree from the following parameters:
        
        Parameter: examples => the rows in the table of examples
        Parameter: attributes => the attribute headers in the table
        Parameter: parent_examples => The examples from the table above
        
        References: Fig. 18.5 "The decision-tree learning algorithm", pg. 702
        www.cs.bham.ac.uk/internal/courses/intro-ai/current/notes.php
        """
        
        # print 'Entering decision_tree_learning...'
        
        # Make a local copy of attrbutes (Python passes by refernece)
        attribute_copy = copy.deepcopy(attributes)
        
        # If none of the parents have the given value of the attribute
        # from the above split...
        if not examples:
            return aLeaf(self.plurality_value(parent_examples)[0])        
        
        # If all examples have same value of the attribute from above split
        elif self.plurality_value(examples)[0] == len(examples):
            return aLeaf(examples[0][0])
        
        # If there isn't a single classification (above), but there aren't
        # any attributes left
        elif not attribute_copy:
            return aLeaf(plurality_value(examples)[1])        
        
        # Else split the tree on the most important attribute, and
        # recurse for each attribute value
        else:
            A = self.choose_attribute(examples)
            tree = aNode(attribute_copy[A])
            attribute_copy.pop(A)
            
            # Create a list of examples that have value vk for attribute A
            children = {}
            child_exs = self.get_children(examples, A)
            for attri, exs in child_exs.iteritems():
                children[attri] = \
                    self.decision_tree_learning(exs, attribute_copy, examples)
            tree.set_children(children)
            return tree
        
    def plurality_value(self, examples):
        """Returns the highest count in examples.  Figure 18.5, pg. 702 """
        number = []
        names = []
        
        for line in examples:
            if line[0] in names:
                i = names.index(line[0])
                number[i] = number[i] + 1
            else:
                names.append(line[0])
                number.append(1)

        return max(number),names[number.index(max(number))]        