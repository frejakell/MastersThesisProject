from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import triplets as tp
import numpy as np
import UPGMA

def triplet_decompose(tree,triplets):
    #print(tree)
    if tree.is_leaf() is False:
        subtrees=tree.get_children()
        #print(subtrees)
        if len(subtrees)>1:
            right_subtree=subtrees[0]
            left_subtree=subtrees[1]
            right_leaves,t=triplet_decompose(right_subtree,triplets)
            left_leaves,t=triplet_decompose(left_subtree,triplets)  
            sub_right= list(combinations(right_leaves,2))
            sub_left= list(combinations(left_leaves,2))
            #print(sub_right)
            #print(sub_left)
            triplets =bulid_list(left_leaves,sub_right,triplets)
            triplets =bulid_list(right_leaves,sub_left,triplets)
            #print(triplets)
        else:
            #print("hjjjj")
            return subtrees[0].name
        leaves=right_leaves+left_leaves
    else:
        #print("hjjjj",tree)
        leaves=[tree.name]

    #print(leaves)
  
    return leaves,triplets
def bulid_list(list1, list2, trips_list):
    
    for x in list1:
        for y in list2:
            
                trips_list.append([x,sorted(y)])
    return trips_list
def main(arg1,arg2): 
    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    #print(t2)
    triplets=[]
    taxa=[]
    leaf_sets=[]
    for i in range(0,len(content)):
        #print(i)
        tree_run=Tree(content[i])
        leaves,triplets=triplet_decompose(tree_run,triplets)
    #print(triplets) 
    


#main("test1.txt",2)