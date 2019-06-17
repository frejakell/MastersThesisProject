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
    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph_good.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph_good[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph_good and node2 in self._graph_good[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph_good:
            return None
        for node in self._graph_good[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
  
    
def clades_from_graph(taxa, graph):
    ##print(taxa) 
    clades_num=0
    clades=[]
    children=[]
    connections=graph._graph_good
    taxa_remainder=set(taxa)
    ##print(taxa_remainder)
    while taxa_remainder:
        
        node=taxa_remainder.pop()
        clades.append([])
        clades[clades_num].append(node)
        ##print(set(connections[node]["good"]))
        overlap=taxa_remainder & set(connections[node]["good"]) 
        taxa_remainder=taxa_remainder-set(overlap)
        
        children=children+list(set(overlap))
        ##print(children)
        while children: 
            
            node=children.pop()
            clades[clades_num].append(node)
            overlap=taxa_remainder & set(connections[node]["good"])
            ##print(overlap)
            #overlap=list(set(taxa_remainder) & set(connections[node]["good"]))
            #children.append(overlap)     
            children=children+list(set(overlap))
            taxa_remainder=taxa_remainder-set(node)-set(overlap)
        clades_num +=1
        
        
    ##print("Clades--------------------------------------------------------------------------")
    ##print(clades)
    return clades
def physic_pc(S,R,triplets_dict): 
    #print(triplets_dict)
    #print(S)
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
    ##print(g._graph_good)
    ##print(bad)
    cc=clades_from_graph(set(taxa), g)
      
    print("graph connects",cc)
    if len(cc)>1:
        Cpc=cc
    else: 
        Rdc=[]
        R_remain=[]
        taxa_remain=[]
        taxa_Rdc=[]
        
        for t in triplets_dict:
            ##print(triplets_dict[t])
            triplet_set=triplets_dict[t]
            if (len(triplet_set) >1):
                Rdc.append(triplet_set[0])
                #Rdc.append()
                R_remain.append(triplet_set[1])
            else:
                R_remain.append(triplet_set)
              
        print("R_dc  :  ",Rdc)
        print("R_remain:  ",R_remain)
        R_good=[]
        R_bad=[]
        for t in R_remain:
            ##print(t)
            R_good.append(t[0][1])
            R_bad.append((t[0][0],t[0][1][0]))
            R_bad.append((t[0][0],t[0][1][1]))
            taxa_remain+=[t[0][0],t[0][1][0],t[0][1][1]]
        g_R_remain = Graph(R_good, R_bad, directed=False)
        cc=clades_from_graph(set(taxa_remain), g_R_remain)
        print(cc)
        if len(cc)==1:
            Cpc=[]
            for e in cc[0]:
                Cpc.append([e])
        else: 
            
            Cpc=cc
            Old_Cpc=[]
            while(Cpc!=Old_Cpc):
                print("I am in here")
                ##print(Old_Cpc)
                Old_Cpc=Cpc
                for t_dc in Rdc:
                    ci=-1
                    cj=-1
                    for i in range(len(Cpc)):
                        cc=Cpc[i]
                        print("triplet",t_dc)
                        print(Cpc)
                        print("comp",cc)
                        if set(t_dc[1]).issubset(cc):
                            ci=i
                        elif(t_dc[0] in cc):
                            cj=i
                    if(ci !=-1 and cj !=-1 and ci != cj):
                        triplets_copy=triplets
                        t_ci=[]
                        for tc in triplets_copy:
                            if set([tc[0],tc[1][0],tc[1][0]]).issubset(Cpc[ci]):
                                t_ci.append(tc)    
                        t_ci_good=[]
                        t_ci_bad=[]
                       
                        for t in t_ci:
                            t_ci_good.append(t[1])
                            t_ci_bad.append((t[0],t[1][0]))
                            t_ci_bad.append((t[0],t[1][1]))
                            taxa_Rdc+=[t[0],t[1][0],t[1][1]]
                        
                        g_t_ci_ = Graph(t_ci_good, t_ci_bad, directed=False)
                        ##print(g_t_ci_._graph_good)
                        New_cc=clades_from_graph(set(Cpc[ci]), g_t_ci_)
                        print("new is ", New_cc)
                        if len(New_cc)>1:
                            del Cpc[ci]
                            Cpc=Cpc + New_cc
                        else:
                            del Cpc[ci]
                            
                            for e in New_cc[0]:
                                ##print("e is:  ---------",e)
                                Cpc.append([e])
    '''if(isinstance(Cpc, str))
        #print Tree(Cpc)
    else:'''
    Trees_found=[]
    #print("CPc is                       ---  +++++",Cpc)
    for ci in Cpc:
        triplets_dict_ci=defaultdict(list)
        t_ci=[]
        taxa_ci=[]
        for tc in triplets:
            if set([tc[0],tc[1][0],tc[1][0]]).issubset(ci):
                t_ci.append(tc)
                taxa_ci +=[tc[0],tc[1][0],tc[1][1]]
                
                trip_key=[tc[1][0],tc[1][1],tc[0]]
                trip_key.sort()
                
                trip_key=str(trip_key).strip('[]')
                trip_key=trip_key.replace("'", '')
                trip_key=trip_key.replace(" ", "")
                if (tc in triplets_dict_ci[trip_key]) is False :
                    triplets_dict_ci[trip_key].append(tc)
        if len(t_ci)<1:
            Ti=Tree()
            if len(ci)==1:
               Ti=ci[0]
            else:
                for v in ci:
                    #print(v)
                    Ti.add_child(name=v)
            Trees_found.append(Ti)
        else:
            ##print(set(taxa_ci),t_ci,triplets_dict_ci)
            Trees_found.append(physic_pc(set(taxa_ci),t_ci,triplets_dict_ci))
    Final_tree=Tree()
    
    for tree in Trees_found:
        ##print(tree)
        if isinstance(tree, str):
            Final_tree.add_child(name=tree)
        else:
            Final_tree.add_child(tree)
    #print("-------------------Trees_found----------------------------")
    #print(Final_tree)
    #print("-------------------tree end----------------------------")
    return Final_tree
    
                    
def main(arg1,arg2): 
    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    ##print(t2)
    triplets=[]
    taxa=[]

    for i in range(0,len(content)): 
        t1=Tree(content[i])
        leaves,triplets=tp.triplet_decompose(t1,triplets)
        t2=Tree(content[i])
        ##print(t2)
        taxa+=leaves
    ##print(triplets)
    triplets_dict=defaultdict(list)

    for t in triplets:

        trip_key=[t[1][0],t[1][1],t[0]]
        trip_key.sort()
        
        trip_key=str(trip_key).strip('[]')
        trip_key=trip_key.replace("'", '')
        trip_key=trip_key.replace(" ", "")
        
        if (t in triplets_dict[trip_key]) is False :
            triplets_dict[trip_key].append(t)
    ##print(triplets_dict)
    Cpc=physic_pc(list(set(taxa)),triplets,triplets_dict)
    print(Cpc)
    Cpc.show()
     

main("test1.txt",2)