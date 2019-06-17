from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
import rf_dist_list
import operator
#import dendropy
import UPGMA_inc 
import UPGMA
from itertools import permutations,product
import numpy as np
#from dendropy_cop.scripts.strict_consensus_merge import strict_consensus_merge
import random,time
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
#def sort_source_trees(content):
def number_labels(start, end):
    labels = []
    for i in range(start, end ):
        labels.append(str(i))
    return labels

def get_unique(a,b):
    unique_list= {*a} ^ {*b}
    #print(a)
    #print(b)
    #print(unique_list)
    return len(unique_list)
def scm(tree1,tree2):
    
    leaf_list1=[]
    leaf_list2=[]
    for leaf in tree1: 
        leaf_list1.append(leaf.name)
    for leaf in tree2: 
        leaf_list2.append(leaf.name)
    ##print(leaf_list1)  
    overlap=intersection(leaf_list1,leaf_list2)
    ##print("overlap is: ",overlap)
    if(len(overlap)<3):
        #print("overlap is: ",overlap)
        return tree2.write(format=9)
    tree1_copy=tree1.copy()
    tree2_copy=tree2.copy()
    tree1_copy.prune(overlap)
    tree2_copy.prune(overlap)

    #t.write(format=1
    splits2=rf_dist_list.main(tree2_copy.copy(),tree1_copy.copy())
    splits1=rf_dist_list.main(tree1_copy.copy(),tree2_copy.copy())
    ##print("splits 1:  ", splits1)
    ##print("splits 2:  ",splits2)
    for lists in splits1:
        node=tree1_copy.get_common_ancestor(lists[0])
        #subtree2=Tree()
        #parent=node.up
        node.delete()
        node=tree1_copy.get_common_ancestor(lists[1])
        node.delete()
    '''for lists in splits2:
        node=tree2_copy.get_common_ancestor(lists[0])
        #subtree2=Tree()
        #parent=node.up
        node.delete()
        node=tree2_copy.get_common_ancestor(lists[1])
        node.delete()'''
    remainder_tree1=set(leaf_list1)-set(overlap)
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
                ##print("now here")
                node.descen.append(leaves)
                #node.descen=arr_descen
                ##print("now here", node.descen)
            else:
                ##print("here!")
                node.add_features(descen=[leaves])
            node=node.up
        node= tree2.search_nodes(name=leaves)[0]
        while node.up:
            
            if hasattr(node,"descen"):
                #arr_descen=node.descen
                ##print("now here")
                node.descen.append(leaves)
                #node.descen=arr_descen
                ##print("now here", node.descen)
            else:
                ##print("here!")
                node.add_features(descen=[leaves])
            node=node.up
    ##print("after pruning:  ", tree1_copy)             
    for node in tree1.traverse("postorder"):
        if hasattr(node,"descen"):
        
            children=node.get_children()
            ##print(children)
            for c in children:
                
                if hasattr(c,"descen") is False:
                   ##print(node.descen)
                   ##print("-------------------------------------------------------")
                   
                   if(len(node.descen)==1):
                       new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                       if(hasattr(new_node.up,"new_child")):
                           
                           node_replace=new_node.up
                          
                           node_replace.add_child(c)
                       else:
                           
                           #new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                           node_replace=new_node.up
                           ##print("tree1",node_replace,c,node.descen)
                           node_change=node_replace.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                           ##print(tree1_copy)
                       #new_node.add_sister(c)
                   else: 
                       new_node=tree1_copy.get_common_ancestor(set(node.descen))
                       ##print(new_node)
                       if( hasattr(new_node.up,"new_child")):
                           new_node=new_node.up
                           new_node.add_child(c) 
                           
                       elif(new_node.up ): 
                           
                           node_change=new_node.up
                           ##print(new_node,c,node.descen)
                           node_change=node_change.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                       else: 
                           new_node=tree1_copy.get_tree_root()
                           if(hasattr(new_node,"new_root")):
                           
                               
                               new_node.add_child(c)
                           else:
                               
                               root_copy=new_node.copy()
                               new_tree=Tree()
                               new_root=new_tree.get_tree_root()
                               new_root.add_features(new_root=True)
                               new_root.add_child(c)
                               new_root.add_child(root_copy)
                               tree1_copy=new_tree
                    
    for node in tree2.traverse("postorder"):
        if hasattr(node,"descen"):
        
            children=node.get_children()
            ##print(children)
            for c in children:
                
                if hasattr(c,"descen") is False:
                   ##print(node.descen)
                   ##print("-------------------------------------------------------")
                   
                   if(len(node.descen)==1):
                       new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                       if(hasattr(new_node.up,"new_child")):
                           
                           node_replace=new_node.up
                           
                           node_replace.add_child(c)
                       else:
                           
                           #new_node=tree1_copy.search_nodes(name=node.descen[0])[0]
                           node_replace=new_node.up
                           ##print("tree1",node_replace,c,node.descen)
                           node_change=node_replace.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                           ##print(tree1_copy)
                       #new_node.add_sister(c)
                   else: 
                       new_node=tree1_copy.get_common_ancestor(set(node.descen))
                       ##print(new_node)
                       if( hasattr(new_node.up,"new_child")):
                           new_node=new_node.up
                           new_node.add_child(c) 
                           
                       elif(new_node.up ): 
                          
                           node_change=new_node.up
                           ##print(new_node,c,node.descen)
                           node_change=node_change.add_child()
                           node_change.add_child(c)
                           node_add_old=new_node.copy()
                           node_change.add_features(new_child=True)
                           node_change.add_child(node_add_old)
                           new_node.detach() 
                       else: 
                           new_node=tree1_copy.get_tree_root()
                           if(hasattr(new_node,"new_root")):
                           
                               
                               new_node.add_child(c)
                           else:
                               
                               root_copy=new_node.copy()
                               new_tree=Tree()
                               new_root=new_tree.get_tree_root()
                               new_root.add_features(new_root=True)
                               new_root.add_child(c)
                               new_root.add_child(root_copy)
                               tree1_copy=new_tree
                           
                       
    ##print("returning tree",tree1_copy)
    return tree1_copy.write(format=9)
    #
    ##print(rf_dist_list.main(tree1_copy,tree2_copy))
def main(arg1, arg2):              
    start_time=time.time()
    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    ##print(content)
    if (arg2 =="common"):
        leaf_lists={}
        for i in range(len(content)):
            t1=Tree(content[i])
            leaf_lists[i]=[]
            for leaf in t1:
               leaf_lists[i].append( leaf.name)
        #print(leaf_lists)
        distance_mat=[]
        for x in range(0,len(content)):
            distance_mat.append([])
            for y in range(0,x):
                lev_dist=len(intersection(leaf_lists[x],leaf_lists[y]))
                distance_mat[x].append(lev_dist)
        #.pop(0)
        M_labels = number_labels(0, len(content))
        tree,order= UPGMA_inc.UPGMA(distance_mat, M_labels)
        #print(tree)
        tree=tree+';'
        t_order=Tree(tree)
        order_list=[]
        for node in t_order.traverse("postorder"):
            # Do some analysis on node
            if node.is_leaf():
                order_list.append(node.name)

        ##print(t_order)
        ##print(order_list)
        #min_x=distance_mat.index(min(distance_mat))
        #min_y=distance_mat[min_x].index(min(distance_mat[min_x]))
        
        ##print(min_x,min_y)
        ##print(distance_mat[min_x][min_y])
        t2=Tree(content[int(order_list[0])])
        for i in range(0,len(order_list)-1): 
            
            t1=Tree(content[int(order_list[i+1])])
            tree1_copy=t1.copy()
            t2=Tree(scm(t1,t2))
           
         
            #splits1=rf_dist_list.main(tree1_copy.copy(),tree2_copy.copy())
            ##print("splits 1:  ", splits1)
            ##print("splits 2:  ",splits2) 
        ##print(t2.write(format=9))
        #t2.show()
    elif (arg2 =="uncommon"):
        leaf_lists={}
        for i in range(len(content)):
            t1=Tree(content[i])
            leaf_lists[i]=[]
            for leaf in t1:
               leaf_lists[i].append( leaf.name)
        ##print(leaf_lists)
        distance_mat=[]
        for x in range(0,len(content)):
            distance_mat.append([])
            for y in range(0,x):
                lev_dist=get_unique(leaf_lists[x],leaf_lists[y])
                distance_mat[x].append(lev_dist)
        #.pop(0)
        M_labels = number_labels(0, len(content))
        tree,order= UPGMA.UPGMA(distance_mat, M_labels)
        ##print(tree)
        tree=tree+';'
        t_order=Tree(tree)
        order_list=[]
        for node in t_order.traverse("postorder"):
            # Do some analysis on node
            if node.is_leaf():
                order_list.append(node.name)

        ##print(t_order)
        #print(order_list)
        #min_x=distance_mat.index(min(distance_mat))
        #min_y=distance_mat[min_x].index(min(distance_mat[min_x]))
        
        ##print(min_x,min_y)
        ##print(distance_mat[min_x][min_y])
        t2=Tree(content[int(order_list[0])])
        for i in range(0,len(order_list)-1): 
            
            t1=Tree(content[int(order_list[i+1])])
            tree1_copy=t1.copy()
            t2=Tree(scm(t1,t2))
           
            leaf_list1=[]
            leaf_list2=[]
            for leaf in t1: 
                leaf_list1.append(leaf.name)
            for leaf in t2: 
                leaf_list2.append(leaf.name)
            ##print(leaf_list1)  
            overlap=intersection(leaf_list1,leaf_list2)
            ##print("overlap is: ",overlap)
            

            tree2_copy=t2.copy()
            ##print(tree1_copy,tree2_copy)
            
            tree1_copy.prune(overlap)
            tree2_copy.prune(overlap)

            #t.write(format=1
            splits2=rf_dist_list.main(tree2_copy.copy(),tree1_copy.copy())
            #splits1=rf_dist_list.main(tree1_copy.copy(),tree2_copy.copy())
            ##print("splits 1:  ", splits1)
            ##print("splits 2:  ",splits2)
    else:
        t2=Tree(content[0])
        for i in range(0,len(content)-1): 
            
            t1=Tree(content[i+1])
            tree1_copy=t1.copy()
            t2=Tree(scm(t1,t2))
           
            leaf_list1=[]
            leaf_list2=[]
            for leaf in t1: 
                leaf_list1.append(leaf.name)
            for leaf in t2: 
                leaf_list2.append(leaf.name)
            ##print(leaf_list1)  
            #overlap=intersection(leaf_list1,leaf_list2)
            ##print("overlap is: ",overlap)
            

            #tree2_copy=t2.copy()
            ##print(tree1_copy,tree2_copy)
            
            #tree1_copy.prune(overlap)
            #tree2_copy.prune(overlap)

            #t.write(format=1
            #splits2=rf_dist_list.main(tree2_copy.copy(),tree1_copy.copy())
            #splits1=rf_dist_list.main(tree1_copy.copy(),tree2_copy.copy())
            ##print("splits 1:  ", splits1)
            ##print("splits 2:  ",splits2)
    ##print(time.time()-start_time)
        ##print(t2.write(format=9))
    t2.show()
    return t2
main("seabirds.txt","uncommon")