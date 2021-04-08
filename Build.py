from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import fast_triplet as tp

class Graph(object):
    """ Graph data structure, undirected by default. """
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
        """ Add connection between node1 and node2 """
        self._graph_good[node1]["bad"].add(node2)
        if not self._directed:
            self._graph_good[node2]["bad"].add(node1)
    def add_weights(self, node1, node2,type):
        """ Add connection between node1 and node2 """
        #if node1 is not None  node2 is not None:
        L=[node1,node2]
        L=sorted(L)
        
        key=str(L[0])+str(L[1])
        self._weights[key][type]=self._weights[key][type]+1

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
  
     
def clades_from_graph(taxa, graph):
     
    clades_num=0
    clades=[]
    children=[]
    connections=graph._graph_good
    taxa_remainder=set(taxa)
    #print(taxa_remainder)
    while taxa_remainder:
        
        node=taxa_remainder.pop()
        clades.append([])
        clades[clades_num].append(node)
        #print(set(connections[node]["good"]))
        overlap=taxa_remainder & set(connections[node]["good"]) 
        taxa_remainder=taxa_remainder-set(overlap)
        
        children=children+list(set(overlap))
        #print(children)
        while children: 
            
            node=children.pop()
            clades[clades_num].append(node)
            overlap=taxa_remainder & set(connections[node]["good"])
            #print(overlap)
            #overlap=list(set(taxa_remainder) & set(connections[node]["good"]))
            #children.append(overlap)     
            children=children+list(set(overlap))
            taxa_remainder=taxa_remainder-set(node)-set(overlap)
        clades_num +=1
        
        
    #print("Clades--------------------------------------------------------------------------")
    #print(clades)
    return clades
        
def build(S,R): 
    #print(R)
    triplets=R
    taxa=S
    if len(S)<3:
        tree_trivial=Tree()
        for leaf in S:
            tree_trivial.add_child(name=str(leaf))
        #tree_trivial.add_child(name=str(S[1]))
        return tree_trivial
    good=[]
    bad=[]
    for t in triplets:
        good.append(t[1])
        bad.append((t[0],t[1][0]))
        bad.append((t[0],t[1][1]))
   
    g = Graph(good, bad, directed=False)  
    #print(g._graph_good)
    #print(bad)
    cc=clades_from_graph(set(taxa), g)
      
    print(cc)
    if len(cc)==1:
        Ter=Tree()
        for c in cc[0]:
            Ter.add_child(name=c)
        return Ter
    else: 
        Tree_CC=Tree()
        for ci in cc:
                #cc=Cpc[i]
                triplets_copy=triplets
                t_ci=[]
                for tc in triplets_copy:
                    if set([tc[0],tc[1][0],tc[1][0]]).issubset(ci):
                        t_ci.append(tc)
                Tci=build(set(ci),t_ci)
                if isinstance(Tci, str) is False:
                    Tree_CC.add_child(Tci)
    return Tree_CC
        
             
                    
def main(arg1,arg2): 
    with open(arg1) as f:
        content = f.readlines()
    
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    #print(t2)
    triplets=[]
    taxa=[]

    for i in range(0,len(content)): 
        t1=Tree(content[i])
        t1.resolve_polytomy()
        leaves,triplets=tp.triplet_decompose(t1,triplets)
        #t2=Tree(content[i])
        #print(t2)
        taxa+=leaves
    #print(set(taxa))
    Cpc=build(list(set(taxa)),triplets)
    #print(Cpc)
    Cpc.show()
    return Cpc
