from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import fast_triplet as tp

class Graph(object):
   
    def __init__(self, connections, bad_con, directed=False):
        self._graph_good =  defaultdict(lambda: defaultdict(set))
        self._weights =  defaultdict(lambda: defaultdict(lambda:0))
        self._directed = directed
        self.add_connections(connections,bad_con)
    
    
        

    def add_connections(self, connections, bad_con):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)
            self.add_weights(node1,node2,"good")
        for node1, node2 in bad_con:
            self.add_bad(node1, node2)
            self.add_weights(node1,node2,"bad")
         
    def add(self, node1, node2):
        """ Add connection between node1 and node2 """
        self._graph_good[node1]["good"].add(node2)
        if not self._directed:
            self._graph_good[node2]["good"].add(node1)
  
    def add_bad(self, node1, node2):
        
        self._graph_good[node1]["bad"].add(node2)
        if not self._directed:
            self._graph_good[node2]["bad"].add(node1)
    def add_weights(self, node1, node2,type):
        
        #if node1 is not None  node2 is not None:
        L=[node1,node2]
        L=sorted(L)
        
        key=str(L[0])+str(L[1])
        self._weights[key][type]=self._weights[key][type]+1
    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

def check_pi(tree,R_pi): 
   
    leaf_list=[]
    for leaves in tree:
        leaf_list.append(leaves.name)
    if len(leaf_list) ==1:
        return tree
    good=[]
    bad=[]
    for key in R_pi:
        t=R_pi[key][0]
        
        good.append(t[1])
        bad.append((t[0],t[1][0]))
        bad.append((t[0],t[1][1]))
    ####print(good)
    ####print(bad)    
    g = Graph(good, bad, directed=False)
    cc=clades_from_graph(set(leaf_list), g)
    if len(cc)==1:
        return "Error"
     
    
    collaps=True
    while(collaps is True):
        subtree=tree.get_children()
        for s in subtree:
            collaps=False
            #s=subtree.pop()
            subtree_leaves=[]
            leaf_list_i=[]
            t_i=[]
            tci_pairs=[]
            for leaves in s:
                subtree_leaves.append(leaves.name)
            for trip in R_pi:
                tc=R_pi[trip][0]
                if set([tc[0],tc[1][0],tc[1][0]]).issubset(subtree_leaves):
                    t_i.append(tc)
                    leaf_list_i.append(tc[0])
                    leaf_list_i=leaf_list_i+ tc[1]
                elif set(tc[1]).issubset(subtree_leaves):
                    tci_pairs.append(tc)
                    
            good=[]
            bad=[]
            for t in t_i:
                good.append(t[1])
                bad.append((t[0],t[1][0]))
                bad.append((t[0],t[1][1]))
           
            g = Graph(good, bad, directed=False)
            cc=clades_from_graph(set(leaf_list_i), g)
            for sj in subtree:
              
                subtree_leaves_j=[]
                t_j=[]
                if sj !=s:
                    
                    for leaves in sj:
                        subtree_leaves_j.append(leaves.name)
                   
                    for tc in tci_pairs:
                        if tc[0] in subtree_leaves_j:
                            t_j.append(tc)
                            leaf_list_i=leaf_list_i+tc[1]
                            
                    good_j=good
                    bad_j=bad
                    for t in t_j:
                        good_j.append(t[1])
                        bad_j.append((t[0],t[1][0]))
                        bad_j.append((t[0],t[1][1])) 
                    g_j = Graph(good_j, bad_j, directed=False)
                    cc_j=clades_from_graph(set(leaf_list_i), g_j)
                    
                    if len(cc_j)>1:
                        subtree_extra=s.get_children()
                        s.delete()
                        
                        subtree=subtree+subtree_extra
                        collaps=True 
                        
                  
    tree_children=tree.get_children()
    new_trees=[]
    R_ti=defaultdict(list)
    for ti in tree_children:
        leaves=[]
        #R_ti=[]
        for leaf in ti:
            leaves.append(leaf.name)
        for trip in R_pi:
            tc=R_pi[trip][0]
            if set([tc[0],tc[1][0],tc[1][0]]).issubset(leaves):
                R_ti[trip].append(tc)
        new_trees.append(check_pi(ti,R_ti))
    final_tree=Tree()
    for Tis in new_trees:
        #if isinstance(Tis,str):
        
        final_tree.add_child(Tis)
  
    return(final_tree)                    
                        

def physic_pi(Tpc,Source_trees):
    Tpi= Tpc
    
    while(new_Tpi != Tpi):
        new_Tpi=Tpi
        
    
def clades_from_graph(taxa, graph):
     
    clades_num=0
    clades=[]
    children=[]
    connections=graph._graph_good
    taxa_remainder=taxa
    while taxa_remainder:
        node=taxa_remainder.pop()
        clades.append([])
        clades[clades_num].append(node)
        ####print(set(connections[node]["good"]))
        overlap=taxa_remainder & set(connections[node]["good"]) 
        taxa_remainder=taxa_remainder-set(overlap)
        
        children=children+list(overlap)
        while children: 
            node=children.pop()
            clades[clades_num].append(node)
            overlap=taxa_remainder & set(connections[node]["good"])
            #overlap=list(set(taxa_remainder) & set(connections[node]["good"]))
            #children.append(overlap) 
            ###print(children)
            #children=children+list(overlap)
            taxa_remainder=taxa_remainder-set(node)
        clades_num +=1
        
    ####print("Clades--------------------------------------------------------------------------")
    ####print(clades)
    return clades
    
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
  
def main(arg1, arg2):              

    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    ####print(t2)
    triplets=[]
    taxa=[]
    good=[]
    bad=[]
    for i in range(1,len(content)): 
        t1=Tree(content[i])
        ####print(t1)
        leaves,triplets=tp.triplet_decompose(t1,triplets)
        #t2=Tree(content[i])
        ####print(t2)
        taxa+=leaves
    Super_triplet=[]
    t2=content[0]
    Super_leaves,Supers_triplets=tp.main(t2,Super_triplet) 
    R_pi=intersection(triplets,Super_triplet)
   
    final_tree=check_pi(R_pi,Tree(t2))
    ###print("final ishhhhhh:          --",final_tree)
   
    
#main("test1.txt",2)