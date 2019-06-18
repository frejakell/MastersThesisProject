from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import triplets as tp
import numpy as np
import flow_algorithm
import random
import time
import scm
import math
from copy import deepcopy

class Graph(object):
    """ Graph data structure, undirected by default. """
    def __init__(self, connections,missing, bad_con, nodes,  directed=False):
        self._graph_good =  defaultdict(lambda: defaultdict(set))
        self._weights =  defaultdict(lambda: defaultdict(lambda:0))
        self._directed = directed
        self._nodes=nodes
        self.add_connections(connections,missing,bad_con)
    
    def delete_leaf(self,node,leaves):
        """ Add connections (list of tuple pairs) to graph """
        good_leaves=intersection(self._graph_good[node]['good'],leaves)
        for leaf in good_leaves:
            set_l=self._graph_good[node]['good']
            set_l.remove(leaf)
            self._graph_good[node]['good']=set_l
        bad_leaves=intersection(self._graph_good[node]['bad'],leaves)
        for leaf in bad_leaves:
            set_l=self._graph_good[node]['bad']
            set_l.remove(leaf)
            self._graph_good[node]['bad']=set_l
        bad_leaves=intersection(self._graph_good[node]['missing'],leaves)
        for leaf in bad_leaves:
            set_l=self._graph_good[node]['missing']
            set_l.remove(leaf)
            self._graph_good[node]['missing']=set_l
    def delete_semi(self,node):
        """ Add connections (list of tuple pairs) to graph """
        connections=self._graph_good[node]['good']
        for c in connections:  
           ##print(c)
           set_l= self._graph_good[c]['good']
           set_l.remove(node)
           self._graph_good[c]['good']=set_l
        connections=self._graph_good[node]['bad']
        for c in connections:  
           ##print(c)
           set_l= self._graph_good[c]['bad']
           set_l.remove(node)
           self._graph_good[c]['bad']=set_l
        dict_reformed=self._graph_good
        del dict_reformed[node] 
        nodes_list=self._nodes
        print(nodes_list,node)
        nodes_list.remove(node)
        self._nodes=nodes_list
        self._graph_good=dict_reformed
        ##print("should be gone",self._graph_good[node])        
    def delete_connections(self,node):
        """ Add connections (list of tuple pairs) to graph """
        connections=self._graph_good[node]['good']
        for c in connections:  
           ##print(c)
           set_l= self._graph_good[c]['good']
           set_l.remove(node)
           self._graph_good[c]['good']=set_l
        connections=self._graph_good[node]['bad']
        for c in connections:  
           ##print(c)
           set_l= self._graph_good[c]['bad']
           set_l.remove(node)
           self._graph_good[c]['bad']=set_l
        dict_reformed=self._graph_good
        del dict_reformed[node] 
        nodes_list=self._nodes
        #print(nodes_list,node)
        #nodes_list.remove(node)
        self._nodes=nodes_list
        self._graph_good=dict_reformed
        ##print("should be gone",self._graph_good[node])
    def delete_leaf_complete(self,l):
       
        good_leaves=self._graph_good[l]['good']
        for node in good_leaves:
            set_l=self._graph_good[node]['good']
        
            set_l.remove(l)
            self._graph_good[node]['good']=set_l
        bad_leaves=self._graph_good[l]['bad']
        for node in bad_leaves:
            set_l=self._graph_good[node]['bad']
            set_l.remove(l)
            self._graph_good[node]['bad']=set_l
        bad_leaves=self._graph_good[l]['missing']
       
        for node in bad_leaves:
            set_l=self._graph_good[node]['missing']
            
            if len(set_l)>1:
                set_l.remove(l)
                self._graph_good[node]['missing']=set_l
        del self._graph_good[l] 
    def add_connections(self, connections,missing, bad_con,):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)
            self.add_weights(node1,node2,"good")
        for node1, node2 in bad_con:
            self.add_bad(node1, node2)
            self.add_weights(node1,node2,"bad")
        for node1, node2 in missing:
            self.add_missing(node1, node2)
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
    def add_missing(self, node1, node2):
        """ Add connection between node1 and node2 """
        self._graph_good[node1]["missing"].add(node2)
        if not self._directed:
            self._graph_good[node2]["missing"].add(node1)
        
        
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

def maxFlow_cut(graph,d_new,last_cs):

    cc=[]
    com_count=0
    clades=[[]]
    leaves=[[]]
    all_clades=[]
    connect_dict={}
    for i in range(len(graph)):
        connect_dict[i]=[]
        for j in range(len(graph)):
            if graph[i][j]>0:
                connect_dict[i].append(j)
    child_remainder=set(range(0,len(graph),1))
    #print(connect_dict[last_cs+2])
    children=connect_dict[last_cs+2]
    connects_set=[]
    leaves_set=[]
    leaves_set.append(d_new[last_cs+2])
    while children: 
        current_child=children.pop()
        child_remainder-= set(str(current_child))
        insetion=connect_dict[current_child]
        #insetion.append(current_child)
        for i in insetion:
            if i> last_cs+1:
                
                leaves_set.append(d_new[i])
                #children.append(j)
                #child_remainer=child_remainer-set([j])
            elif(d_new[i][-1] !='-'):
                
                connects_set.append(d_new[i])
                #children.append(j)
               # child_remainer=child_remainer-set([j])
            
            new_set=intersection(connect_dict[i],child_remainder)
            children+=new_set
            child_remainder-= set(new_set)
    #print(leaves_set)
    #print(connects_set)
    leaves[com_count].append(set(leaves_set))
    all_clades +=connects_set
    clades[com_count].append(set(connects_set))
    com_count+=1
    leaves.append([])
    clades.append([])
    leaves_set=[]
    connects_set=[]
    for i in child_remainder:
            if i> last_cs+1:
                
                leaves_set.append(d_new[i])
                #children.append(j)
                #child_remainer=child_remainer-set([j])
            elif(d_new[i][-1] !='-'):
                
                connects_set.append(d_new[i])
                #children.append(j)
               # child_remainer=child_remainer-set([j])
    leaves[com_count].append(set(leaves_set))
    all_clades +=connects_set
    clades[com_count].append(set(connects_set))
    """            
    #print(connect_dict)

    components=set(range(0,len(graph),1))
    child_remainer=set(range(0,len(graph),1))
    #print(child_remainer)
    cc=[]
    com_count=-1
    clades=[]
    leaves=[]
    all_clades=[]
    while child_remainer:
        Current=child_remainer.pop()
        cc.append([])
        leaves.append([])
        clades.append([])
        com_count+=1
        children=[]
        children.append(Current)
 
        connects_set=[]
        leaves_set=[]
        cc[com_count].append(d_new[Current])
        if Current>last_cs+1:
            leaves_set.append(d_new[Current])
        elif(d_new[Current][-1] !='-'):
            connects_set.append(d_new[Current])
        while children:
            cur_child=children.pop()
            ##print(cur_child)
            for j in range(len(graph[cur_child])):
                if ((graph[cur_child][j]>0) and (j in child_remainer)):
                    
                    cc[com_count].append(d_new[j])
                    if j> last_cs+1:
                        
                        leaves_set.append(d_new[j])
                        children.append(j)
                        child_remainer=child_remainer-set([j])
                    elif(d_new[j][-1] !='-'):
                        
                        connects_set.append(d_new[j])
                        #children.append(j)
                       # child_remainer=child_remainer-set([j])
                    
                    
            
            children=list(set(children))
        
    #print("leaves are: ",leaves)
    #print("clades are: ",clades)
    """
    
    return set(all_clades),leaves,clades
def connections_div(graph,taxa):
     
    clades_num=0
    clades=[]
    children=[]
    all_clades=[]
    network=graph._graph_good
    #taxa_remainder=set(taxa)
    ##print("---------------------------------------------network-----------------------------------------------------------------")
    ##print(network)
    taxa_remain=set(taxa)
    taxa_seen=set()
    counter=0
    clades_connects=[]
    new_connect_clade=[]
    #connects_set=[]
    while(taxa_remain):
        
        clades.append([])
        clades_connects.append([])
        current_taxa=taxa_remain.pop()
        current_taxa_set=set()
        
        connections=set(network[current_taxa]["good"])
        ##print("---------------------------------------------taxa_set-----------------------------------------------------------------")
        ##print( taxa_remain)
        ##print(taxa_set)
        #connections_remain
        new_clade=[]
        new_clade.append(current_taxa)
        connections_seen=set(connections)
        while connections:
            counter+=1 
            ##print("before",len(connections))
            current_connections=connections.pop() 
            ##print("after",current_connections ) 
            new_taxa_set=set(network[current_connections]["good"]) #taxa
            #taxa_seen +=new_taxa_set
            for n in new_taxa_set:
                ##print("taxa",n)
                new_clade.append(n)
                taxa_connect=set(network[n]["good"])#connect
                
                taxa_connect=taxa_connect-connections_seen
                new_connect_clade+=taxa_connect
                ##print("seen aere",connections_seen)
                ##print("current",connections)
                ##print(counter,taxa_connect)
                connections.update(taxa_connect) 
                
                connections_seen.update(taxa_connect)
            ##print("updated",new_taxa_set)
            taxa_seen.update(new_taxa_set) 
            taxa_remain =taxa_remain-taxa_seen
            ##print(counter,connections_seen)
             ##print(counter,taxa_connect)
            #taxa_set=set(connections[node]["good"])
            #connections_remain -= new_node_set
        #all_clades+=list(set(new_connect_clade))
        
        clades[clades_num].append(set(new_clade))
        connects_set=[]
        #clades_connects.append([])
        for leaf in new_clade:
            connects_set += network[leaf]["good"]
            all_clades += network[leaf]["good"]
        
        clades_connects[clades_num].append(set(connects_set))
        clades_num+=1 
    return clades,clades_connects,set(all_clades)
def find_semiUni(graph):
    semi=[]
    nodes=graph._nodes
    #print("nodes are",nodes)
    connections=graph._graph_good
    for n in nodes:
        #print("semi test",connections[str(n)]["bad"])
        if len(connections[str(n)]["bad"])==0:
            semi.append(str(n))
    return semi
def make_mrp(tree,a,d,missing_taxa,counter):
   
    ##print(tree)
    if tree.is_leaf() is True:
        leaves=[tree.name]
        return leaves,a,counter
    else:
        b = np.zeros(shape=(len(d),1))
        subtrees=tree.get_children()
        ##print(subtrees)
        if len(subtrees)>1:
            right_subtree=subtrees[0]
            left_subtree=subtrees[1]
            right_leaves,a,counter=make_mrp(right_subtree,a,d,missing_taxa,counter)
            left_leaves,a,counter=make_mrp(left_subtree,a,d,missing_taxa,counter)  
        else:
            
            return subtrees[0].name,a,counter

        leaves=right_leaves+left_leaves
        for ml in missing_taxa:
            b[d[ml],0]=2
       
        for cl in leaves:
            b[d[cl],0]=1
        if counter !=0:
            ##print(b)
            a=np.append(a, b, axis=1 )
        else:
            ##print(b)
            a=b
            counter=1

  
    return leaves,a,counter
def BCD(graph,taxa):
    newick=""
    #print("taxa are",taxa)
    ##print("taxa set : ",taxa)
    ##print(graph._graph_good)
    ##print(graph._graph_good)
    if len(taxa)==0:
        return "error"
    if(len(taxa)<3  ):
        ##print("here")
        if len(taxa)<2:
            leaf=taxa.pop()
            return leaf
        else:
            tree_new=Tree()
            for leaf in taxa:
                newick+= leaf + "," 

            ##print("done")
       # #print(tree_new)
        return "("+ newick+")"
    else:
        tree_new=Tree()
        ##print("plot_start",time.time())
        semi=find_semiUni(graph)
        ##print("plot_stop",time.time())
        for sem in semi:
            graph.delete_semi(str(sem))
            #print("semi",sem)
        ##print(graph._graph_good)
        clades,clades_connects,all_clades=connections_div(graph,taxa)
        ##print(all_clades)
        ##print(clades)
        ##print(clades_connects)
        if len(clades)==1: 
            g_HS=deepcopy(graph)
            
            all_clades,clades,clades_connects=plot_HS(g_HS,taxa)
            ##print(g_HS)
            
            ##print(comp_div)
            g_HS=None
            ##print("final",cuts_final)
            #connect_nodes= set(connect_nodes)-set([cuts_final[0][0][1]])
            #graph.delete_connections(cuts_final[0][0][1])
            ##print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            ##print(graph._graph_good)
            #clades,clades_connects,all_clades=connections_div(graph,taxa)
            
            #print("leaves: ",clades)
            #
        for ci in range(len(clades)):
           
            clade=clades_connects[ci]
            ci_taxa=clades[ci] 
            #print("all_clades complete list", all_clades)
            #print("taxa complete list", taxa)
            #print("connections list in it  ",clade)
            #print("taxa list in it  ",ci_taxa)
            g_ci=deepcopy(graph)
            delete_clade=set(all_clades)-clade[0]
            delete_leaves=taxa-ci_taxa[0]
            
            #print("leaves to delete",delete_leaves)
            #print("connects to delete",delete_clade)
            for c in delete_clade:
                #print("cladestep",c)
                g_ci.delete_connections(c)
        
            for l in delete_leaves:
                g_ci.delete_leaf_complete(l)
            ##print(g_ci._graph_good)
            newick+=BCD(g_ci,ci_taxa[0])
            
        ##print("plot_start",time.time())
        ##print(tree_new)
        return '(' + newick + ")" 
        
def plot_HS(graph,taxa):
    current_set=[]
    for keys in graph._graph_good:
        
        if keys.isdigit():
            current_set.append(keys)
            current_set.append(keys + str("-"))   
        elif keys in taxa:
            current_set.append(keys)
    current_set=sorted(current_set)
    #print(current_set)
    d_new= {}
    for i in range(len(current_set)):
        d_new[current_set[i]]=i
    ##print(d_new)
    #hs=np.zeros(shape=(len(d_new),len(d_new)))
    cur_g=graph._graph_good
    
    test_graph=[]
    counter=0
    for i in range(len(current_set)):
        test_graph.append([])
        
        for i in range(len(current_set)):
            test_graph[counter].append(0)
        counter+=1 
    last_cs=0
    current_set=sorted(current_set)
    ##print("current_set",current_set)
    counter=0
    connect_nodes=[]
    for i in range(len(current_set)):
        counter+=1 
        cur_key=current_set[i]
        
        if cur_key.isdigit():
            ##print(cur_key)
            connect_nodes.append(cur_key)
            test_graph[d_new[cur_key+"-"]][d_new[cur_key]]=len(graph._graph_good[cur_key]["bad"])
            ##print("key cell :",test_graph[d_new[cur_key+"-"]][d_new[cur_key]])
            last_cs=i
        connects=cur_g[cur_key]["good"]
        for c in connects:
            test_graph[d_new[cur_key]][d_new[c]]= 1
            if cur_key.isdigit():
                test_graph[d_new[c]][d_new[cur_key+"-"]]= 1
    #print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")   
    ##print(test_graph)
    ##print(hs)
    cuts_final=[]
    comp=-1
    cuts=[]
    min_cut_cost=float('inf')
    min_cut=[]
    
    ##print("strart",current_set[last_cs+2])
    counter_it=0
    #print(time.time())
    for i in range(last_cs+3,len(current_set)):
        ##print("new",current_set[i])
        ##print("plot_start",time.time())
        print(i)
        
        cut_graph=deepcopy(test_graph)
        cuts=flow_algorithm.main(cut_graph,last_cs+2,i)

        cut_graph=None
        print("don")
        current_cut=0
        ##print("cut was", cuts)
        if len(cuts)>0:
            cuts_final.append([])
            comp+=1
        for c in cuts:
            if len(c) >0:
               
               cuts_final[comp].append([current_set[c[0]], current_set[c[1]]])
               current_cut+=test_graph[c[0]][c[1]]
        if current_cut<min_cut_cost:
            min_cut=cuts 
            min_cut_cost=current_cut
    #print(time.time())
    #print("cut is :", min_cut)
    cc=[]
    leaves=[[],[]]
    clades=[[],[]]

    print(d_new)
    for cut in min_cut:
        test_graph[int(cut[0])][int(cut[1])]=0
        """
        #
        ##print(test_graph[int(cut[0])][int(cut[1])])
        i=cut[0]
        if int(i)> last_cs+1:
                
            leaves[0].append(current_set[i])
            #children.append(j)
            #child_remainer=child_remainer-set([j])
        elif(current_set[i][-1] !='-'):
            clades[0].append(current_set[i])
            cc.append(current_set[i])
        j=cut[1]
        if int(j)> last_cs+1:
                
            leaves[1].append(current_set[j])
            #children.append(j)
            #child_remainer=child_remainer-set([j])
        elif(current_set[j][-1] !='-'):
            clades[1].append(current_set[j])
            cc.append(current_set[j])"""
    cc,leaves,clades=maxFlow_cut(test_graph,current_set,last_cs)
    print(cc,leaves,clades)
    return cc,leaves,clades
def main(arg1,arg2): 

    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    tree2=Tree(content[0])
    ##print(t2)
    triplets=[]
    taxa=[]
    leaf_sets=[]
    for i in range(0,len(content)): 
    
        taxa_tree=[]
        t2=Tree(content[i])
        for leaf in t2:
            taxa_tree.append(leaf.name)
        leaf_sets.append(taxa_tree)
        taxa+=list(taxa_tree)
        tree1=Tree(content[i])
        ##print("start_tree1",t1)
        ##print("start_tree2",t2)
        tree2=Tree(scm_last.scm(tree1,tree2))
    ##print(tree2)
    merge_taxa=[]
    merge_count=0
    merge_lookup={}
    for node in tree2.traverse("postorder"):

  # Do some analysis on node
        if (node.is_root() is False) and (node.is_leaf() is False):
            children=node.get_children()
            if len(children) >2:
                merge_taxa.append([])
                for c in children:
                    if c.is_leaf():
                        merge_taxa[merge_count].append(c.name)
                        merge_lookup[c.name]=merge_count
                merge_count +=1 
    ##print(merge_taxa)
    ##print(merge_lookup)
    taxa=set(taxa)
    d = {ni: indi for indi, ni in enumerate(set(taxa))}
    inv_map = {v: k for k, v in d.items()}

    ##print(d,inv_map)
    a=0
    counter=0
    #a[:] = '?'
    for i in range(0,len(content)): 

        t2=Tree(content[i])
        missing_taxa=set(taxa)-set(leaf_sets[i])
        tree_right=t2.get_children()[0]
        tree_left=t2.get_children()[1]
        temp_r,a,counter=make_mrp(tree_right,a,d,missing_taxa,counter)
        temp_l,a,counter=make_mrp(tree_left,a,d,missing_taxa,counter)
        
    connections=[]
    missing=[]
    bad_connect=[]
    ##print(len( a.T))
    counter=0
    int_nodes=range(1, len( a.T)+1)
    node=[]
    for i in int_nodes:
        node.append(str(i))
    for column in a.T:
       ##print("#print column",column)
       counter +=1
       for i in range(len(column)):
            if column[i]== 1:
                ##print(inv_map[i])
                #if inv_map[i] in merge_lookup:
                    ##print("look up is", merge_taxa[merge_lookup[inv_map[i]]])
                    
                connections.append([str(counter),inv_map[i]])
                connections.append([inv_map[i],str(counter)])
                
            elif column[i]== 2:
                ##print(inv_map[i])
                missing.append([str(counter),inv_map[i]])
            else:
                bad_connect.append([str(counter),inv_map[i]])
    ''' semi=[]
    counter=0
    for column in a.T:
        counter +=1
        ##print(column)
        if(np.prod(column)!=0):
            semi.append(counter)'''
    ##print(connections)
    g=Graph(connections,missing,bad_connect,node)  
    ##print(g._graph_good)
    #hs_size=len(d)+counter-len(semi)
    tree_new=Tree()
    semi=find_semiUni(g)
    for sem in semi:
        g.delete_semi(str(sem))
        ##print("semi:",sem)
    ##print(g._graph_good[])
    ##print("plot_start",time.time())
    clades,clades_connects,all_clades=connections_div(g,taxa)
    ##print("plot_stop",time.time())
    ##print("all is",all_clades)
    ##print(len(clades))
    if len(clades)==1: 
        
        g_HS=deepcopy(g)
        all_clades,clades,clades_connects=plot_HS(g_HS,taxa)
        g_HS=None
 
        #print(clades)
        #print(clades_connects)
        ##print(g._graph_good)
    ##print("all clade",clades)
    newick=""
    for ci in range(len(clades_connects)):
        clade=clades_connects[ci]
        ci_taxa=clades[ci]
        g_ci=deepcopy(g)
       
        delete_clade=set(all_clades)-clade[0]
        delete_leaves=taxa-ci_taxa[0]

        #print(delete_leaves)
        for c in delete_clade:
             ##print("cladestep",c)
             g_ci.delete_connections(c)
        
        for l in delete_leaves:
            g_ci.delete_leaf_complete(l)
        ##print("deleted clades",delete_clade)
        ##print("deltetd leaes",delete_leaves)
        ##print("clades keep",clade[0])
        ##print("leaves keep",ci_taxa[0])
        ##print(g_ci._graph_good)
        #BCD(g_ci,ci_taxa[0])
        
        #tree=BCD(g_ci,ci_taxa[0])
        newick+=BCD(g_ci,ci_taxa[0])
        #if tree != "error":
            #tree_new.add_child(tree)
    newick="("+ newick+");"
    print(newick)
    tree_new.show()
main("test1.txt",2)    
