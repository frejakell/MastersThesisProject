from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import triplets as tp
import numpy as np
import UPGMA

def triplet_decompose(tree,triplets,triplets_dict):
    ##print(tree)
    if tree.is_leaf() is False:
        subtrees=tree.get_children()
        ###print(subtrees)
        complete=[]
        for leaf in subtrees:
            if leaf.is_leaf() is True:
                complete.append(leaf.name)
        if len(subtrees)>1:
            for i in range(len(subtrees)): 
                
                sub_leaves,t,triplets_dict=triplet_decompose(subtrees[i],triplets,triplets_dict)
                sub_comb= list(combinations(sub_leaves,2))
                rest_leave=set(complete)-set(sub_leaves)
                triplets =bulid_list(rest_leave,sub_comb,triplets)
                ##print(sub_leaves)
                ##print(sub_comb)
                ##print(complete)
                ##print("trip",triplets)
          
            '''right_subtree=subtrees[0]
            left_subtree=subtrees[1]
            right_leaves,t,triplets_dict=triplet_decompose(right_subtree,triplets,triplets_dict)
            left_leaves,t,triplets_dict=triplet_decompose(left_subtree,triplets,triplets_dict)  
            sub_right= list(combinations(right_leaves,2))
            sub_left= list(combinations(left_leaves,2))
            ###print(sub_right)
            ###print(sub_left)
            triplets =bulid_list(left_leaves,sub_right,triplets)
            triplets =bulid_list(right_leaves,sub_left,triplets)'''

            for t in triplets:

                trip_key=[t[1][0],t[1][1],t[0]]
                trip_key.sort()
                
                trip_key=str(trip_key).strip('[]')
                trip_key=trip_key.replace("'", '')
                trip_key=trip_key.replace(" ", "")
                
                if (t in triplets_dict[trip_key]) is False :
                    triplets_dict[trip_key].append(t)
                    
            leaves=complete
        else:
            ###print("hjjjj")
            return subtrees[0].name
        
    else:
        ###print("hjjjj",tree)
        leaves=[tree.name]

    ##print(triplets_dict)
  
    return leaves,triplets,triplets_dict
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
    ###print(t2)
    triplets=[]
    taxa=[]
    leaf_sets=[]
    triplets_dict=defaultdict(list)
    for i in range(0,len(content)):
        ###print(i)
        tree_run=Tree(content[i])
        leaves,triplets=triplet_decompose(tree_run,triplets,  leaf_sets,triplets_dict)
    ###print(triplets) 
    


#main("test1.txt",2)