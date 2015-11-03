"""
Trilobite (The abstRact manIpuLation Of BInary TreEs) is a library written in Python and Java which contains high-level routines for binary tree search, insertion, removal and replacement. 
"""
import math
from math import *


# Example output:
#     A
#    / \
#   B   C
#  / \ /
# c   d

# l =2
#  A
# / \
#b   c
"""
This method prints a binary heap in tree form.
E.g:

Abc
is rendered as
  A
 / \
b   c

ABCde f
is rendered as
     A
    / \
   /   \
  B     C
 / \     \
d   e     f


RATBCY de fgh
is rendered as
           R
          / \
         /   \
        /     \
       /       \
      /         \
     A           T
    / \         /
   /   \       /
  B     C     Y
 / \     \   / \
d   e     f g   h
"""
def print_tree(tree_str,display_slashes=True):
    # Compute the depth of the tree: a tree with l levels has binary heap size 2^l -1.
    l = int(ceil(log(len(tree_str)+1,2)));
    #Fill in the tree string with blank spaces:
    tree_length= 2**l - 1;
    tree_str += ' '*(tree_length-len(tree_str));
    #pos_array holds the column number that each character is meant to be printed in
    pos_array=[-1]*tree_length;
    #pos_array[0]=l*(l+1) /2 -1;
    #Initialise the positions of the leftmost diagonal; from these positions
    #the positions of all the other characters may be calculated.
    for index in range(0,l):
        pos_array[2**index -1] = int(floor((3* 2**(l-index-2) -1)))
    
    #Now fill in the rest of the positions:
    for index in range(0,tree_length):
        if pos_array[index] == -1:
            curr_level=int(ceil(log(index+2,2)))-1
            parent_pos=pos_array[(index+1)/2  -1];
            #pos_array[index] = 2*pos_array[index/2 -1] - pos_array[index-1]
            if index % 2: #If the index is odd; we must move to the left of the parent index
                pos_array[index]=parent_pos - int(ceil(3* 2 **(l-2-curr_level)))
            else: #The index is even so we must move to the right of the parent index
                pos_array[index]=parent_pos + int(ceil(3* 2 **(l-2-curr_level)))
    #print('depth=%d'%l)
    #print(pos_array);
    #print('tree_str: %s' %tree_str);
    #Store the output lines in a text array:
    #output_lines=[' '*(pos_array[-1]+1)]*(l*(l+1)/2)
    
    #Store the output lines in a text array:
    #output_lines=[t[:] for t in [[' ']*(pos_array[-1]+1)]*l];
    #Load over all characters to be rendered
    #for index in range(tree_length):
        #Calculates the level of the current character to be printed
     #   char_level= int(ceil(log(index+2,2)))-1;
        #print(curr_line_index)
     #   output_lines[curr_line_index][pos_array[index]]=tree_str[index];
            
    
    #Store the output lines in a text array:
    output_lines=[t[:] for t in [[' ']*(pos_array[-1]+1)]*l];
    for index in range(tree_length):
    #Calculate the index of the line that the current character should be printed to:
        curr_line_index= int(ceil(log(index+2,2)))-1;
        #print(curr_line_index)
        output_lines[curr_line_index][pos_array[index]]=tree_str[index];
        #print(output_lines);

    if display_slashes: #We need to add some slashes first
        output_lines_with_slashes=[t[:] for t in [[' ']*(pos_array[-1]+1)]*int(floor((3 * 2**(l-2))))];
        #Easier to start from the bottom of the list and link up:
        output_lines.reverse();
        output_lines_with_slashes[0]=output_lines[0];
        curr_line_index=1;
        for index in range(1,int(floor((3 * 2**(l-2))))):
            #The algorithm builds up a line of slashes.
            #If two slashes cross, then it must be necessary to print a new level of the tree.
            previous_line=output_lines_with_slashes[index-1];
            add_new_level_flag=False
            prev_level_left_slashes= [i for i in range(len(previous_line)) if previous_line[i] == '\\'] #Source: 
                    #<http://stackoverflow.com/questions/11122291/python-find-char-in-string-can-i-get-all-indexes>
            prev_level_right_slashes= [i for i in range(len(previous_line)) if previous_line[i] == '/']
            prev_level_letters=[i for i in range(len(previous_line)) if previous_line[i].isalpha()] ##isalpha returns True if and only if n[i] is a letter
            for i in prev_level_left_slashes:
                output_lines_with_slashes[index][i-1]='\\'; #Add another left slash
            for i in prev_level_right_slashes:
                if output_lines_with_slashes[index][i+1] == ' ':
                    output_lines_with_slashes[index][i+1]='/';
                else:
                    add_new_level_flag=True
            for i in prev_level_letters:
                letter_sign = tree_str.find(previous_line[i]) %2;# Too hacky; doesn't allow for duplicate letters!
                if letter_sign: #We need to add a right slash 
                    if output_lines_with_slashes[index][i+1] == ' ':
                        output_lines_with_slashes[index][i+1]='/'
                    else:
                        add_new_level_flag=True
                else:
                    if output_lines_with_slashes[index][i-1] == ' ':
                        output_lines_with_slashes[index][i-1]='\\'
                    else:
                        add_new_level_flag=True
           
            if add_new_level_flag:
                #print('curr_line_index=%s'%curr_line_index)
                output_lines_with_slashes[index]=output_lines[curr_line_index];
                curr_line_index=1+curr_line_index;
        #print('Displaying slashes yet to be implemented')

        # Now reverse the lines:
        output_lines_with_slashes.reverse()
        for line in output_lines_with_slashes:
            print("".join(line));
    else:
        #Just print the lines to the output:
            for line in output_lines:
                print("".join(line));




"""
Convenience method to help with string searching.

"""
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]
