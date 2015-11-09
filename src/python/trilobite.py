"""
Trilobite (The abstRact manIpuLation Of BInary TreEs) is a library written in Python and Java which contains high-level routines for binary tree search, insertion, removal and replacement. 
"""
import math
import random

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
    #Trim any empty children (blank spaces) that may be at the end of the tree.
    tree_str=tree_str.rstrip();
    #Terminate upon being given a blank tree
    if len(tree_str) ==0:
        return;
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
          

def subtree(tree_str,n):
    """
Returns the subtree of a binary heap starting at position n.
E.g. subtree(RATBCY de fgh,1) will return ABCde f
    """
    tree_str=tree_str.rstrip();
    tree_size=len(tree_str)
    subtree_size= int(math.floor((2*tree_size - n)/float(2+n))) +1; 
    #+1 due to counting 0 as an index.
    # This formula gives a value which is slightly too high; try to work out an
    # analytic formula for the size of the subtree but it probably isn't possible.

    #Have a lower bound too
    #subtree_lower_bound=int(math.floor((tree_size - n)/float(1+n))) ; 



    #print("Upper bound for subtree size: %s"%subtree_size)
    #print("Lower bound for subtree size: %s"%subtree_lower_bound)

    # Initialise the subtree:
    subtree=[' ' for i in range(subtree_size)]
    for i in range(subtree_size):
        a_i = int((n * 2**math.floor(math.log(i+1,2)) )+i);
        if a_i>=tree_size: # We have already calculated all the coefficients;
            #print("Actual subtree size: %s"%i)
            return "".join(subtree[:i])# trim the subtree to size and return it.
        else:
            subtree[i]=tree_str[a_i];

    #Return the subtree
    #print("Actual subtree size: %s "%subtree_size)
    return "".join(subtree);


def randtree(p_blank=0.05,alphabet=[chr(i) for i in range(ord('a'), ord('z') + 1)],unique_nodes=True,max_levels=6):
    """
Generates a random tree.
    """
    alphabet=alphabet[:];
    if unique_nodes: #If we need unique nodes, we should shuffle the alphabet and draw the letters one by one.
        random.shuffle(alphabet)
    #print(alphabet)
    tree = []; #Use a character array to build the tree; more efficient than string concatenation.
    # Keep track of where we are in the tree.
    curr_index=0;
    # Need to keep track of the last filled position in the tree in order to figure out if we have 
    # finished or not.
    last_occupied_index=0;
    if p_blank==0 and not unique_nodes:
        print('warning - p_blank=0 and unique_nodes=False - returning a blank tree')
        return '';
    #if not unique_nodes:
    #    print('unique_nodes=False not yet implemented')
    #    return;
    #We want to loop until either all nodes
    # in the current level of the tree have no children or if the number of levels in the tree
    # has reached max_levels.
    while curr_index <=2*last_occupied_index+2 and (max_levels <0 or curr_index <= 2**(max_levels) -2): 
        # First, check whether we need to add a new leaf.
        # If we are at the root (position 0) or if the parent node is blank we can skip over it.

        if curr_index==0 or not tree[(curr_index+1)/2  -1] == ' ': #Add a new node
            node_is_blank=random.random()<p_blank
            if node_is_blank:
                tree.append(' ')
            else:
                if unique_nodes: #Unique nodes, so we need to remove a character from the alphabet without replacement.
                    if len(alphabet) >0:
                        tree.append(alphabet.pop(0));
                        last_occupied_index=curr_index
                    else: #If no other letters are left, return the tree.
                        return "".join(tree);
                else:
                    tree.append(random.choice(alphabet));
                    last_occupied_index=curr_index
        else:
            tree.append(' ')
        curr_index=curr_index+1;
    return "".join(tree)


def tree_depth(tree_str):
    """
    Returns the depth of a tree represented in binary heap form.
    """
    tree_str=tree_str.rstrip();
    if len(tree_str) ==0:
        return 0;
    else:
        return int(1+math.floor(math.log(len(tree_str),2)))

def tree_size(tree_str):
    """
    Returns the size of the tree (number of elements).
    """
    return len(tree_str.replace(" ",""))


def traverse(tree_str,mode):
    """
    Traverses a binary tree in a particular order.
    Current options are:
    'pre' - Preorder traversal
    'in' - Inorder traversal
    'post' - Postorder traversal
    """
    if mode == 'bh': # Binary heap
        return tree_str.rstrip();
    elif mode == 'pre' or mode== 'post' or mode =='in': #Preorder traversal
        tree_str=list(tree_str);
        tree_str_len = len(tree_str);
        ret_seq=[];
        curr_index=0
        while True:
            if mode == 'pre':
                if tree_str[curr_index] !=' ': #tree[curr_index] is not blank
                    ret_seq.append(tree_str[curr_index]);
                    #print(tree_str[curr_index])
                    tree_str[curr_index]=' ';
                    if 2*curr_index + 1 < tree_str_len and tree_str[2*curr_index+1]!= ' ':
                       curr_index= 2*curr_index +1;
                       continue
            
                if 2*curr_index + 2 < tree_str_len and tree_str[2*curr_index+2]!= ' ':
                   curr_index= 2*curr_index +2;
                   continue
            elif mode == 'post':
                if tree_str[curr_index] !=' ': #tree[curr_index] is not blank
                    if 2*curr_index + 1 < tree_str_len and tree_str[2*curr_index+1]!= ' ':
                        curr_index= 2*curr_index +1;
                        continue
                    if 2*curr_index + 2 < tree_str_len and tree_str[2*curr_index+2]!= ' ':
                        curr_index= 2*curr_index +2;
                        continue
                    ret_seq.append(tree_str[curr_index]);
                    #print(tree_str[curr_index])
                    tree_str[curr_index]=' ';
            elif mode == 'in':
                if tree_str[curr_index] !=' ': #tree[curr_index] is not blank
                    if 2*curr_index + 1 < tree_str_len and tree_str[2*curr_index+1]!= ' ':
                        curr_index= 2*curr_index +1;
                        continue
                    ret_seq.append(tree_str[curr_index]);
                    #print(tree_str[curr_index])
                    tree_str[curr_index]=' ';
                
            
                if 2*curr_index + 2 < tree_str_len and tree_str[2*curr_index+2]!= ' ':
                    curr_index= 2*curr_index +2;
                    continue
            if curr_index ==0:
                return "".join(ret_seq);
            else:
                curr_index = (curr_index+1)/2  -1

