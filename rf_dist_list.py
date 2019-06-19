#!/usr/bin/python
from ete3 import Tree, TreeStyle, Tree, TextFace, add_face_to_node,NodeStyle
import random
from Bio import SeqIO
from Bio.Align.Applications import ClustalOmegaCommandline
import sys
from subprocess import call
from Bio.Align.Applications import MuscleCommandline

rfdist = 0
leaf_num = 0 

def getRandomNode(tree):
    return tree.get_leaf_names()[random.randint(0, len(tree.get_leaves())-1)]
        

def readFasta(fasta_file):
    return list(SeqIO.parse(fasta_file, "fasta"))
                
def check_what_algorithm(alg, in_file, out_file):
    if alg == "CLUSTAL":
        clustalomega_cline = ClustalOmegaCommandline(infile=in_file, outfile = out_file, verbose=True, auto=True)
        return clustalomega_cline
    elif alg.upper() == "KALIGN":
        return 0
     
def main(arg1, arg2):
    list_splits1=[]
    list_splits2=[]
    t1=Tree()
    tree1=arg1
    
    tree2=arg2

    node_midpoint = getRandomNode(tree1)
   
    tree1.set_outgroup(node_midpoint)
    
    tree2.set_outgroup(node_midpoint)
    
    
    t1, tree2=tree2.get_tree_root().children
    t1, tree1=tree1.get_tree_root().children
    count = 0
    for leaf in tree1.traverse("postorder"):
        if(leaf.name.strip()):
            count += 1
            leaf.add_features(order=count)
            CurrentNode2=tree2&leaf.name
            CurrentNode2.add_features(order=count)
            
        elif(leaf.name!=node_midpoint):
            leaf.name="int"
            
   
    
    for node in tree2.traverse("postorder"):
        if(node.name==""):
            node.name="int"
    
    Num_splits1=0
    Num_splits2=0
    Num_shared=0
   
    for node in tree1.traverse("postorder"):
        list_leaves=[]
        if((node.name=="int")):
            Num_splits1+=1
            cmin=float("+inf")     
            cmax=0
            subtree=Tree()
            for d1 in node.get_children():
                subtree.add_child(d1)
            
            
            #subtree.add_child(d2)
            ##print(subtree)
            for leaf in subtree:
                list_leaves.append(leaf.name)
                if ((leaf.name!="int") and (leaf.name!="")):
                    
                    ##print("leaf name",leaf.name)
                    CurrentNode2=tree1&leaf.name
                    cmin=min( CurrentNode2.order, cmin)
                    cmax=max( CurrentNode2.order, cmax)
                    
            if((node.is_root()==False)):
                node.name="["+str(cmin)+":"+str(cmax)+"]" 
                list_splits1.append(sorted(list_leaves))
                
    for node in tree2.traverse("postorder"):
        list_leaves=[]
        if((node.name=="int") and (node.is_root()==False)):
            Num_splits2+=1
            cmin=float("+inf")    
            cmax=0
            size=0
            #d1,d2=node.get_children()
            subtree2=Tree()
            for d1 in node.get_children():
                subtree2.add_child(d1)
            #subtree2.add_child(d1)
            #subtree2.add_child(d2)
            
            for leaf in subtree2:
                size+=1
                list_leaves.append(leaf.name)
                if ((leaf.name!="int") and (leaf.name!=node_midpoint) and (leaf.name!="")):
                    CurrentNode2=tree2&leaf.name
                    cmin=min( CurrentNode2.order, cmin)
                    cmax=max( CurrentNode2.order, cmax)
            if(size==(cmax-cmin+1)):
                node.name="["+str(cmin)+":"+str(cmax)+"]" 
            if(tree1.search_nodes(name=node.name)):
                Num_shared+=1
                list_splits1.remove(sorted(list_leaves))
            else:
                list_splits2.append(sorted(list_leaves))
            
    global leaf_num 
    ts = TreeStyle()
    ts.show_leaf_name = True
   
    style1 = NodeStyle()
    style1["hz_line_color"] = "#ff0000"
   
    leaf_num = len(tree2.get_leaves())    
    

    rf_dist=Num_splits1+Num_splits2-(2*Num_shared)
    tree1=arg1
    L=[]
    for leaf in tree1:
        L.append(leaf.name)
    L=sorted(L)
    splits_list=[]
    for i in list_splits1:
        rem=set(L)-set(i)
        rem=list(rem)
        splits_list.append([i,rem])
    
    ##print(list_splits1)
    ##print(list_splits2)
   
    ##print(rf_dist)  
    return splits_list
   

    
