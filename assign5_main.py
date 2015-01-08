##############################################################################
# Jason Maynard
# U30503758
# Assignment 5
##############################################################################
# This is the main driver program.  It calls functions and classes from 
# assign5_learning.py
#
# References: 
# My AI group - Nataliya Ivanova, Josh Philpott. 
# The supporting website for the book found at http://aima.cs.berkeley.edu
# http://www.cs.bham.ac.uk/internal/courses/intro-ai/current/notes.php
# 
##############################################################################

import assign5_classes as learn
import copy  # https://docs.python.org/2/library/copy.html

# Get the data ---------------------------------------------------------------
try:
    with open ("input.txt") as the_file:
        
        # Split the input file up by lines
        the_data = the_file.readline().strip().splitlines()
       
        # Get the attribut names from the first row
        temp = the_data[0]
        attribute_names = temp.split()
                
        training_data = []
        test_data = []
        flag = False
        
        for line in range(1, len(the_data)):
            if the_data[line] == '':
                flag = True
            if not flag:  # if we haven't seen a blank line it's training 
                training_data.append(the_data[line].split())
            else:
                if the_data[line] != '':
                    test_data.append(the_data[line].split())           
                                    
except:
    print 'Error: Could not open input.txt'
            
print '\nAttributes:'
for line in attribute_names:
    print line

print '\nTraining data:'
for line in training_data:
    print line
    
print '\nTest data:'
for line in test_data:
    print line
           
def classify_test_examples(line, tree, attribute_names):
    """This function does the classification of test data based
    on the training data."""
    
    # Create a local copy of the attribute names 
    attribute_name_copy = copy.deepcopy(attribute_names)
    
    # When we get down to a leaf we return the value of the leaf.
    if tree.is_leaf():
        return tree.value
    
    # Otherwise 
    else:
        attribute_name = tree.split_name
        i = attribute_name_copy.index(attribute_name)
        sub_tree = tree.children[line[i-1]]
        line.pop(i-1)
        attribute_name_copy.pop(i)
        return classify_test_examples(line, sub_tree, attribute_name_copy)

# Instantiate decision tree object    
decision_tree = learn.aTree()

# Recusively get the tree based on 
# Fig. 18.5 "The decision-tree learning algorithm", pg. 702 
tree = decision_tree.decision_tree_learning(training_data, attribute_names)

# Now test the data based on the tree we built

print '\nThe classification results for the test data:'
for line in test_data:
    print classify_test_examples(line, tree, attribute_names)


        