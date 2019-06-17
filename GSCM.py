from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
import rf_dist_list
import operator
#import dendropy
from itertools import permutations,product
import numpy as np
#from dendropy_cop.scripts.strict_consensus_merge import strict_consensus_merge
import random
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
    
def scm(tree1,tree2):
    leaf_list1=[]
    leaf_list2=[]
    for leaf in tree1: 
        leaf_list1.append(leaf.name)
    for leaf in tree2: 
        leaf_list2.append(leaf.name)
    #print(leaf_list1)  
    overlap=intersection(leaf_list1,leaf_list2)
    #print("overlap is: ",overlap)
    # print(tree1)
    #print(tree2)
    tree1_copy=tree1.copy()
    tree2_copy=tree2.copy()
    tree1_copy.prune(overlap)
    tree2_copy.prune(overlap)
    #t.write(format=1
    #print("tree1 after prune",tree1_copy)
    #print("tree2 after prune",tree2_copy)
    splits2=rf_dist_list.main(tree2_copy.copy(),tree1_copy.copy())
    splits1=rf_dist_list.main(tree1_copy.copy(),tree2_copy.copy())

    for lists in splits1:
        node=tree1_copy.get_common_ancestor(lists[0])
        #subtree2=Tree()
        #parent=node.up
        node.delete()
        node=tree1_copy.get_common_ancestor(lists[1])
        node.delete()
    for lists in splits2:
        node=tree2_copy.get_common_ancestor(lists[0])
        #subtree2=Tree()
        #parent=node.up
        node.delete()
        node=tree2_copy.get_common_ancestor(lists[1])
        node.delete()
    remainder_tree1=set(leaf_list1)-set(overlap)
    #print("Tree1 after deletes",tree1_copy)
    #print("Tree2 after deletes",tree2_copy)
    #for r in remainder_tree1:
        
    remainder_tree2=set(leaf_list2)-set(overlap)
    root1=tree1.get_tree_root()
    root1.add_features(descen=overlap)
    root2=tree2.get_tree_root()
    root2.add_features(descen=overlap)
    for leaves in overlap:
        node= tree1.search_nodes(name=leaves)[0]
        while node.up:
            
            if hasattr(node,"descen"):
                #arr_descen=node.descen
                #print("now here")
                node.descen.append(leaves)
                #node.descen=arr_descen
                #print("now here", node.descen)
            else:
                #print("here!")
                node.add_features(descen=[leaves])
            node=node.up
        node= tree2.search_nodes(name=leaves)[0]
        while node.up:
            
            if hasattr(node,"descen"):
                #arr_descen=node.descen
                #print("now here")
                node.descen.append(leaves)
                #node.descen=arr_descen
                #print("now here", node.descen)
            else:
                #print("here!")
                node.add_features(descen=[leaves])
            node=node.up
    #print(tree1_copy)             
    for node in tree1.traverse("postorder"):
        if hasattr(node,"descen"):
            children=node.get_children()
            #print(children)
            for c in children:
                
                if hasattr(c,"descen") is False:
                   #print(node.descen)
                   #print("-------------------------------------------------------")
                   new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                   if(len(node.descen)==1):
                       if(hasattr(new_node.up,"new_child")):
                           node_replace=new_node.up
                           #print("tree1",node_replace,c,node.descen)
                           node_replace.add_sister(c)
                       else:
                           #new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                           node_replace=new_node.up
                           #print("tree1",node_replace,c,node.descen)
                           node_change=node_replace.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                           #print(tree1_copy)
                       #new_node.add_sister(c)
                   else: 
                       new_node=tree1_copy.get_common_ancestor(set(node.descen))
                       #print(new_node)
                       if(new_node.up and hasattr(new_node.up,"new_child")):
                           new_node=new_node.up
                           new_node.add_child(c) 
                           #print("first")
                       elif(new_node.up): 
                           #new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                           node_replace=new_node.up
                           #print("tree1",node_replace,c,node.descen)
                           node_change=node_replace.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                           #print(tree1_copy
                       else: 
                           #print("thrid")
                           new_node.add_child(c)
                       
                       #print("-------------------------------------------------------")
    for node in tree2.traverse("postorder"):
        if hasattr(node,"descen"):
            children=node.get_children()
            for c in children:
                if hasattr(c,"descen") is False:
                   #print("-------------------------------------------------------")
                   if(len(node.descen)==1):
                       new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                       if( hasattr(new_node.up,"new_child")):
                           #print("tree2",new_node.up,c,node.descen)
                           #new_node.add_sister(c)
                           node_replace=new_node.up
                           #print("tree1",node_replace,c,node.descen)
                           node_replace.add_sister(c)
                           #new_node.add_sister(c)
                       else:
                           
                           node_change=new_node.up
                           #print("tree2",node_change,c,node.descen)
                           #node_change=node_replace.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                       
                       #new_node.add_sister(c)
                   else:
                       new_node=tree1_copy.get_common_ancestor(set(node.descen))
                       #print(new_node)
                       if(hasattr(new_node.up,"new_child")):
                           #print("first")
                           new_node=new_node.up
                           new_node.add_child(c) 
                       elif(new_node.up): 
                           #new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                           node_replace=new_node.up
                           #print("tree1",node_replace,c,node.descen)
                           node_change=node_replace.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                           #print(tree1_copy
                       else: 
                           new_node.add_child(c)
                           #print("thrid")  
                       #print("-------------------------------------------------------")
                
        
    #tree1_copy.show()
    return tree1_copy
    #print(tree2_copy)
    #print(rf_dist_list.main(tree1_copy,tree2_copy))
def main(arg1, arg2):              

    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    #print(t2)
    dict_taxa= defaultdict(list)
    for i in range(1,len(content)): 
        
        t1=Tree(content[i])
        
        for leafs in t1:
            dict_taxa[i].append(leafs.name)
     for trees in 
        #print("start_tree1",t1)
        #print("start_tree2",t2)
      
    print(dict_taxa)
        
main("test1.txt",2)