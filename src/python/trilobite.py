"""
Trilobite (The abstRact manIpuLation Of BInary TreEs) is a library written in Python and Java which contains high-level routines for binary tree search, insertion, removal and replacement. 
"""
import math

def print_tree(tree_str,display_slashes=True,output_file=None):
    """
    This method prints a binary heap in tree form.
    E.g:
    
    Abc \n
    is rendered as \n
      A\n     / \\\n    b   c\n

    ABCde f
    is rendered as
         A\n        / \\\n       /   \\\n      B     C\n     / \     \\\n    d   e     f\n


    RATBCY de fgh
    is rendered as
               R\n              / \\\n             /   \\\n            /     \\\n           /       \\\n          /         \\\n         A           T\n        / \         /\n       /   \       /\n      B     C     Y\n     / \     \   / \\\n    d   e     f g   h\n
    """
    # Compute the depth of the tree: a tree with l levels has binary heap size 2^l -1.
    l = int(math.ceil(math.log(len(tree_str)+1,2)));
    #Fill in the tree string with blank spaces:
    tree_length= 2**l - 1;
    tree_str += ' '*(tree_length-len(tree_str));
    #pos_array holds the column number that each character is meant to be printed in
    pos_array=[-1]*tree_length;
    #Initialise the positions of the leftmost diagonal; from these positions
    #the positions of all the other characters may be calculated.
    for index in range(0,l):
        pos_array[2**index -1] = int(math.floor((3* 2**(l-index-2) -1)))
    
    #Now fill in the rest of the positions:
    for index in range(0,tree_length):
        if pos_array[index] == -1:
            curr_level=int(math.ceil(math.log(index+2,2)))-1
            parent_pos=pos_array[(index+1)/2  -1];
            #pos_array[index] = 2*pos_array[index/2 -1] - pos_array[index-1]
            if index % 2: #If the index is odd; we must move to the left of the parent index
                pos_array[index]=parent_pos - int(math.ceil(3* 2 **(l-2-curr_level)))
            else: #The index is even so we must move to the right of the parent index
                pos_array[index]=parent_pos + int(math.ceil(3* 2 **(l-2-curr_level)))
    #Store the output lines in a text array:
    output_lines=[t[:] for t in [[' ']*(pos_array[-1]+1)]*l];
    #Keep track over which nodes are left-pointing and which are right-pointing:
    output_lines_flags=[t[:] for t in [[-1]*(pos_array[-1]+1)]*l];
    for index in range(tree_length):
    #Calculate the index of the line that the current character should be printed to:
        curr_line_index= int(math.ceil(math.log(index+2,2)))-1;
        #print(curr_line_index)
        output_lines[curr_line_index][pos_array[index]]=tree_str[index];
        output_lines_flags[curr_line_index][pos_array[index]]=index%2;
        #print(output_lines);
    #print(output_lines_flags)
    if display_slashes: #We need to add some slashes first
        output_lines_with_slashes=[t[:] for t in [[' ']*(pos_array[-1]+1)]*int(math.floor((3 * 2**(l-2))))];
        #Easier to start from the bottom of the list and link up:
        output_lines.reverse();
        output_lines_flags.reverse();
        output_lines_with_slashes[0]=output_lines[0];
        curr_line_index=1;
        for index in range(1,int(math.floor((3 * 2**(l-2))))):
            #The algorithm builds up a line of slashes.
            #If two slashes cross, then it must be necessary to print a new level of the tree.
            previous_line=output_lines_with_slashes[index-1];
            add_new_level_flag=False
            prev_level_left_slashes= [i for i in range(len(previous_line)) if previous_line[i] == '\\'] #Source: 
                    #<http://stackoverflow.com/questions/11122291/python-find-char-in-string-can-i-get-all-indexes>
            prev_level_right_slashes= [i for i in range(len(previous_line)) if previous_line[i] == '/']
            prev_level_letters=[i for i in range(len(previous_line)) if not (previous_line[i] == '/' or previous_line[i] == '\\' or previous_line[i]==' ' )]
            for i in prev_level_left_slashes:
                output_lines_with_slashes[index][i-1]='\\'; #Add another left slash
            for i in prev_level_right_slashes:
                if output_lines_with_slashes[index][i+1] == ' ':
                    output_lines_with_slashes[index][i+1]='/';
                else:
                    add_new_level_flag=True
            for i in prev_level_letters:
                #letter_sign = tree_str.find(previous_line[i]) %2;# Too hacky; doesn't allow for duplicate letters!
                letter_sign=output_lines_flags[curr_line_index-1][i]
                #if letter_sign == -1:
                #    print('warning')
                #    print('curr_line_index=%s'%curr_line_index)
                #    print('i=%s'%i)
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

            if curr_line_index <len(output_lines):
                next_line=output_lines[curr_line_index];
                next_line_char_indices=[i for i in range(len(next_line)) if not (next_line[i]==' ' )]
                curr_output_line_indices=[i for i in range(len(output_lines_with_slashes[index])) if not (output_lines_with_slashes[index][i]==' ' )]
                if not set(curr_output_line_indices).isdisjoint(set(next_line_char_indices)):
                    add_new_level_flag=True

           
            if add_new_level_flag:
                output_lines_with_slashes[index]=output_lines[curr_line_index];
                curr_line_index=1+curr_line_index;

        # Now reverse the lines:
        output_lines_with_slashes.reverse()
        
        #Update output_lines:
        output_lines=output_lines_with_slashes;

        if output_file==None: #Just print the lines to the output:
            for line in output_lines:
                print("".join(line));
        else: #Write to file
            for line in output_lines:
                output_file.write("".join(line)+'\n');
            output_file.close()
          

