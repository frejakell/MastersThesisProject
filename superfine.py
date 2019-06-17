from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import random
import scm as scm
import MaxCut
import fast_triplet as tp
import fast_triplet_dictionary as tp_d
import math
#import build
def intersection(lst1, lst2): 
    
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
            

def main(arg1, arg2):  
    with open(arg1) as f:
            content = f.readlines()
            
    triplets=[]
    taxa=[]
    good=[]
    bad=[]
    for i in range(0,len(content)): 
        #####print(i)
        t1=Tree(content[i])
        t1.resolve_polytomy()
        #####print(t1.write(format=9))
        leaves,triplets=tp.triplet_decompose(t1,triplets)
        #t2=Tree(content[i])
        #####print(t2)
        #####print(triplets) 
        taxa+=leaves
    taxa_com=set(taxa)   
    #####print(triplets) 
    d = {ni: indi for indi, ni in enumerate(taxa)}
    rows, cols = (len(taxa), len(taxa)) 
    triplets_dict=defaultdict(list)

    for t in triplets:

        trip_key=[t[1][0],t[1][1],t[0]]
        trip_key.sort()
        
        trip_key=str(trip_key).strip('[]')
        trip_key=trip_key.replace("'", '')
        trip_key=trip_key.replace(" ", "")
        if (t in triplets_dict[trip_key]) is False :
       
            triplets_dict[trip_key].append(t)
    #t2=MaxCut.main(arg1, arg2)
    t2,overlap_per1,inconsist_per1,triplets_dict1=MaxCut.main(arg1,2)
    print("-------------------------------------bulid-------------------------------------------------")
    trees=[]
    t2.show()
    for node in t2.traverse("postorder"):
        children_node=node.get_children()
        
        if len(children_node)>2:
            trees+=children_node
    trees.append(t2)        
    #print(trees)
    taxa=[]
    dict_leaves={}
    for i in range(len(trees)):
        c=trees[i]
        c.detach()
        
        for leaves in c:
            if leaves.name !='':
                dict_leaves[leaves.name]=i
                taxa.append(leaves.name)

    newick_supertrees=[]
    ###print("last tree",trees[len(trees)-1])
    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    for i in range(0,len(content)-2): 
        
        t1=Tree(content[i+1])
        t1.resolve_polytomy()
        for leaves in t1:
            leaves.name="leaf"+ str(dict_leaves[leaves.name])
        
        for i in range(len(trees)):
            current_leaf_set = t1.search_nodes(name="leaf"+str(i))
            #####print(current_leaf_set)
            if len(current_leaf_set)>1:
                for j in range(1, len(current_leaf_set)):
                    current_leaf_set[j].delete()
                
                
        newick_supertrees.append(t1.write(format=9))    
    #####print(newick_supertrees)
    trees_structure,overlap_per1,inconsist_per1,triplets_dict1=MaxCut.main(newick_supertrees,1)

    #####print("------------structure-------------")
    #####print(overlap_per,inconsist_per)
    #####print(trees_structure)
    for i in range(len(trees)):
        node_add=trees_structure.search_nodes(name="leaf"+str(i))
        if len(node_add)>0:
            node_add=node_add[0]
            
            node_add_parent=node_add.up
            ###print(trees[i])
            node_add_parent.add_child(trees[i])
            node_add.detach()
    taxa=set(taxa)
   
    
    final_taxa=[]
    for nodes in trees_structure:
        if nodes.is_leaf():
            if nodes.name !='':
                final_taxa.append(nodes.name)
    
    trees_structure.prune(final_taxa)
    trees_structure.show()
    supertree_triplets=[]
    ST_triplets_dict=defaultdict(list)
    st_leaves,supertree_triplets,ST_triplets_dict=tp_d.triplet_decompose(trees_structure,supertree_triplets,ST_triplets_dict)
    total=1
    #triplets_dict=defaultdict(list)
    overlap=0
    inconsist=0
    for keys in triplets_dict:
        overlap += len(intersection(triplets_dict[keys],ST_triplets_dict[keys]))
        total+=len(triplets_dict[keys])
        if len(triplets_dict[keys])>1:
            inconsist+=len(triplets_dict[keys])
    overlap_per=overlap/total
    inconsist_per=inconsist/total 
    #####print(taxa_com)
    ##print(trees_structure)
    return trees_structure,overlap_per,inconsist_per
main("seabirds.txt",1)