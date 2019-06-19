from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import fast_triplet as tp
import fast_triplet_dictionary as tp_d
import itertools
import sphere
import random 
import math
#import triplet_test
class Graph(object):

    def __init__(self, connections, bad_con, good_mat, bad_mat,d_taxa, directed=False):
        self._graph_good =  defaultdict(lambda: defaultdict(set))
        self._weights =  defaultdict(lambda: defaultdict(lambda:0))
        self._directed = directed
        self._good_mat=good_mat
        self._bad_mat=bad_mat
        self._d_taxa=d_taxa
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
def partition (list_in,n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]
def combine2(lst, n):
    return [list(x) for x in itertools.combinations(lst, n)]   
def findCut(taxa,graph,d): 
    weights=graph._weights
    good_cuts_full=graph._good_mat
    bad_cuts_full=graph._bad_mat
    ####print(graph._graph_good)
    ####print(good_cuts_full)
    ####print(bad_cuts_full)
    
    r=int(math.sqrt(len(taxa)))
    s=r*2+1
    AA,positions=sphere.main(s,r)
    ####print(AA)
    #shuffled_taxa = shuffle(taxa)
    taxa_displament={}
    for t in taxa:
        taxa_displament[t]=random.choice(positions)
    ####print(taxa_displament)
    counter=1
    while counter < 100:
        
        current_node=random.choice(list(taxa))
        ####print(current_node)
        cm_bot=[0,0,0]
        cm_top=[0,0,0]
        
        cm_count=0
        cm_node=taxa_displament[current_node]
        for tc in taxa:
            cm_count+=1
            if tc != current_node:
                cm_tc = taxa_displament[tc]
                bad_current=bad_cuts_full[d[tc]][d[current_node]]
                good_current=good_cuts_full[d[tc]][d[current_node]]
                if bad_current != 0:
                    protion=good_current/bad_current
                    #cm_distance=[abs(y-x) for x, y in zip(cm_node, cm_tc)]
                    ####print(cm_distance)
                    ####print(protion)
                    cm_weight= [protion*x for x in cm_tc]
                    cm_top=[x+y for x, y in zip(cm_top, cm_weight)]
                    cm_bot=[x+y for x, y in zip(cm_bot, cm_tc)]
                    ####print(cm_tc)
                    ####print(cm_bot)
        #cm_adjust= [x/cm_count for x in cm]
        ####print(cm_bot)
        ####print(cm_top)
        new_pos=[]
        for i in range(0,2):
            
            if cm_top[i]>0:
                new_pos.append(cm_top[i]/cm_bot[i])
            else:
                new_pos.append(0)
        taxa_displament[current_node]= new_pos

        
        counter +=1
    thers=int(math.sqrt(s))
    cut_pos_list=range(thers,thers*2)
    slice_list=range(0,2)
    cuts_L=[]
    cuts_R=[]
    count=0
    
    cuts_L=[]
    cuts_R=[]

    cut_pos=random.choice(cut_pos_list)
    slice=random.choice(slice_list)
   
   
    for td in taxa_displament:
        if(taxa_displament[td][slice])<cut_pos:
            cuts_L.append(td)
            
        else:
            cuts_R.append(td)
    
        ####print(taxa_displament)
        count+=1 
    if len(cuts_L)< len(cuts_R):
        cuts_L_temp=cuts_L
        cuts_L=cuts_R
        cuts_R=cuts_L_temp
    cut_cost=0
   
    for leaf_L in  cuts_L:
        for leaf_R in cuts_R:  
            bad_current=bad_cuts_full[d[leaf_L]][d[leaf_R]]
            good_current=good_cuts_full[d[leaf_L]][d[leaf_R]]
            if(bad_current>0):
                cut_cost +=  good_current/bad_current
            else:
                cut_cost +=  good_current
            
   


    swap_taxa=None       
       
   
    swap_taxa_final=0
    while swap_taxa_final==0:
        swap_taxa=None
        swap_taxa_R=None
        delta=0
        delta_R=0
        for i in range(0,len(cuts_L)-1):
            
            leaf_L=cuts_L[i]
            loss_cut=0
            gain_cut=0
            for leaf_R in cuts_R:  
                bad_current=bad_cuts_full[d[leaf_L]][d[leaf_R]]
                good_current=good_cuts_full[d[leaf_L]][d[leaf_R]]   
                if(bad_current>0):
                    loss_cut +=  good_current/bad_current
                else:
                    loss_cut +=  good_current
            for leaf_L_rem in cuts_L:  
                bad_current=bad_cuts_full[d[leaf_L]][d[leaf_L_rem]]
                good_current=good_cuts_full[d[leaf_L]][d[leaf_L_rem]]
                if(bad_current>0):
                    gain_cut +=  good_current/bad_current
                else:
                    gain_cut +=  good_current
                
            cut_change=gain_cut-loss_cut
            if cut_change > delta:
                delta =cut_change 
                swap_taxa=i 


        for i in range(0,len(cuts_R)-1):
            
            leaf_R=cuts_R[i]
            loss_cut=0
            gain_cut=0
            for leaf_L in cuts_L:  
                bad_current=bad_cuts_full[d[leaf_L]][d[leaf_R]]
                good_current=good_cuts_full[d[leaf_L]][d[leaf_R]]   
                if(bad_current>0):
                    loss_cut +=  good_current/bad_current
                else:
                    loss_cut +=  good_current
            for leaf_R_rem in cuts_R:  
                bad_current=bad_cuts_full[d[leaf_R]][d[leaf_R_rem]]
                good_current=good_cuts_full[d[leaf_R]][d[leaf_R_rem]]
                if(bad_current>0):
                    gain_cut +=  good_current/bad_current
                else:
                    gain_cut +=  good_current
                
            cut_change=gain_cut-loss_cut
            if cut_change > delta:
                delta_R =cut_change 
                swap_taxa_R=i 



        if swap_taxa!= None or swap_taxa_R != None :
            ####print(i)
            ####print(cuts_L)
            if(delta_R <delta):
                cuts_R.append(cuts_L[swap_taxa])
                cuts_L= cuts_L[:swap_taxa] + cuts_L[swap_taxa+1 :]
            else:
                cuts_L.append(cuts_R[swap_taxa_R])
                cuts_R= cuts_R[:swap_taxa_R] + cuts_R[swap_taxa_R+1 :]
        else:
            swap_taxa_final=None
    ####print("connection is -------------------------------------------------------------")
    ####print([cuts_L,cuts_R])
    return [cuts_L,cuts_R]
    '''
    
    connections=graph._graph_good
    ####print(connections)
    ####print("weights is -------------------------------------------------------------")
   
    ####print(weights['ab']['good'])
    d=graph._d_taxa
    a = list(taxa) 
    Max_cut=""
    Max_ratio=0
    i=2
    while(i <= int(len(a)/2)+1):
        ###print(i)
        comb=combine2(a,i)
        for c in comb: 
            ####print(c)
            cut_set= set(taxa)-set(c)
           
            good_cuts=0
            bad_cuts=0
            for  pairs in list(product(c, cut_set)):
                #L=[pairs[0],pairs[1]]
                #L=sorted(L)
                #key=str(L[0])+str(L[1])
                good_cuts +=good_cuts_full[d[pairs[0]]][d[pairs[1]]]
                bad_cuts +=bad_cuts_full[d[pairs[0]]][d[pairs[1]]]
            if(bad_cuts/good_cuts > Max_ratio):
                Max_cut= [c,cut_set]
                Max_ratio= bad_cuts/good_cuts
        i+=1
    return Max_cut'''
    
             
def combine2(lst, n):
    return [list(x) for x in itertools.combinations(lst, n)]             
 
def clades_from_graph(taxa, graph):
     
    clades_num=0
    clades=[]
    children=[]
    connections=graph._graph_good
    taxa_remainder=set(taxa)
    ####print(taxa_remainder)
    while taxa_remainder:
        
        node=taxa_remainder.pop()
        clades.append([])
        clades[clades_num].append(node)
        ####print(set(connections[node]["good"]))
        overlap=taxa_remainder & set(connections[node]["bad"]) 
        taxa_remainder=taxa_remainder-set(overlap)
        
        children=children+list(set(overlap))
        ####print(children)
        while children: 
            
            node=children.pop()
            clades[clades_num].append(node)
            overlap=taxa_remainder & set(connections[node]["bad"])
            ####print(overlap)
            #overlap=list(set(taxa_remainder) & set(connections[node]["good"]))
            #children.append(overlap)     
            children=children+list(set(overlap))
            taxa_remainder=taxa_remainder-set(node)-set(overlap)
        clades_num +=1
        
        
    ####print("Clades--------------------------------------------------------------------------")
    ####print(clades)
    return clades
        
    

       
def Max_cut(taxa, trip_d):
    
   
    #connections=graph._graph_good
    t = Tree()
    ####print(taxa)
    if len(taxa)==2:
        # Creates an empty tree
        #node=t.add_child()
        taxa=list(taxa)
        A = t.add_child(name=taxa[0]) # Adds a new child to the current tree root
        # and returns it
        B = t.add_child(name=taxa[1])
        return t
    if len(taxa)==1:
        leaf=taxa.pop()
        #t.add_child(name=leaf)
        return leaf 
    triplets=[] 
    good=[]
    bad=[]
    d = {ni: indi for indi, ni in enumerate(taxa)}
    rows, cols = (len(taxa), len(taxa)) 
    triplets_dict=defaultdict(list)
    good_mat = [[0 for i in range(cols)] for j in range(rows)]    
    bad_mat = [[0 for i in range(cols)] for j in range(rows)] 
    for keys in trip_d:
        words = keys.split(',')
        ####print(words)
        if(set(words).issubset(set(taxa))):
            triplets=trip_d[keys]
            for tri in triplets:
                if bad_mat[d[tri[1][0]]][d[tri[1][1]]] <1:
                    bad.append(tri[1])
                if good_mat[d[tri[0]]][d[tri[1][0]]]<1:
                    good.append((tri[0],tri[1][0]))
                if good_mat[d[tri[0]]][d[tri[1][1]]]<1:
                    good.append((tri[0],tri[1][1]))
                bad_mat[d[tri[1][0]]][d[tri[1][1]]] += 1
                bad_mat[d[tri[1][1]]][d[tri[1][0]]] += 1
                good_mat[d[tri[0]]][d[tri[1][0]]] += 1
                good_mat[d[tri[0]]][d[tri[1][1]]] += 1
                good_mat[d[tri[1][0]]][d[tri[0]]] += 1
                good_mat[d[tri[1][1]]][d[tri[0]]] +=1
    taxa=set(taxa)   
    ####print(triplets) 
   
     
        
    
    ####print(good)
    ####print(bad)    
    g = Graph(good, bad,good_mat,bad_mat, d, directed=False)
    cc=clades_from_graph(set(taxa), g)
 
    cc_cut=cc
    ####print(cc)
    if len(cc_cut) >1: 
        for c in cc_cut:
            sub_t=Max_cut(c,trip_d)
            ####print(sub_t)
            if isinstance(sub_t,str):
                t.add_child(name=sub_t)
            else:
                t.add_child(sub_t)
    else:

        ####print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[")
        cut=findCut(set(taxa),g,d)
        ####print(cut)
        for c in cut:
            new_child=Max_cut(c,trip_d)
            if isinstance(new_child,str):
                t.add_child(name=new_child)
            else:
                t.add_child(new_child)
    return t
    
    
        
    

def decomp(tree,taxa,l_sibs,l_og):
    L=[]
    for leaf in tree:
        L.append(leaf.name)
    L=sorted(L)
    taxa= taxa+L
    all_comb=list(combinations(L,3))
    for comb in all_comb:
        anc1= tree.get_common_ancestor(comb[0], comb[1])
        anc2 = tree.get_common_ancestor(comb[0], comb[2])
        anc3= tree.get_common_ancestor(comb[2], comb[1])
    for node in tree.traverse("postorder"):
        # Do some analysis on node
        if node.is_leaf() is False:
            leaves=node.iter_descendants("postorder")
            leaves_name=[]
            for leaf in leaves:
                leaves_name.append(leaf.name)
            ####print(leaves_name)
            outgroups=set(L)-set(leaves_name)
            l_sibs.append(' '.join(leaves_name).split())
            l_og.append(' '.join(outgroups).split())
    return taxa,l_sibs, l_og
         

def intersection(lst1, lst2): 
    
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
            

    
def main(arg1, arg2):              
    if arg2 == 2:
        with open(arg1) as f:
            content = f.readlines()
    else:
        content = arg1
    ####print(content)
    # you may also want to remove whitespace characters like `\n` at the end of each line
    #content = [x.strip() for x in content] 
    t2=Tree(content[0])
    #print(t2)
    triplets=[]
    taxa=[]
    good=[]
    bad=[]
    for i in range(0,len(content)): 
        ####print(i)
        t1=Tree(content[i])
        #t1.show()
        ###print(t1.write(format=9))
        t1.resolve_polytomy()
        for leaf in t1:
            if leaf.is_leaf() is True:
                taxa.append(leaf.name)
        leaves,triplets=tp.triplet_decompose(t1,triplets)
        #print("leaves",leaves)
        #t2=Tree(content[i])
        
        ####print(triplets) 
        #taxa+=leaves
    taxa=set(taxa)   
    #print(triplets)
    #print("taxa",taxa)
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
    #print(triplets_dict)
    ####print(good)
    ####print(bad)    

    

 
    
    ####print(clades)
    ####print("__________________________________________________________")
    ####print(outgroup)
    #g = Graph(connections, outgroup, good, bad, directed=True)
    ####print(g._graph_good)     
    ####print(g._weights)    
    #triplets_dict=defaultdict(list)
    supertree=Max_cut(taxa, triplets_dict) 
    #print("supertree",supertree)
    #supertree.show()
    '''supertree_triplets=[]
    ST_triplets_dict=defaultdict(list)
    st_leaves,supertree_triplets,ST_triplets_dict=tp_d.triplet_decompose(supertree,supertree_triplets,ST_triplets_dict)
    total=1
    
    overlap=0
    inconsist=0
    for keys in triplets_dict:
        overlap += len(intersection(triplets_dict[keys],ST_triplets_dict[keys]))
        total+=len(triplets_dict[keys])
        if len(triplets_dict[keys])>1:
            inconsist+=len(triplets_dict[keys])
    overlap_per=overlap/total
    inconsist_per=inconsist/total
    #t2=Tree("((ah, ((ae, ab), ai)), ((ag, aa), (ac, (ad, (aj, af)))));")
    ####print(t2)
    #triplet_test.main(arg1,supertree,True,25)
    ##print(supertree)'''
    return supertree,0,0,triplets_dict
    #clades_from_graph(taxa, g)
