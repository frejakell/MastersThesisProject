from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict
from itertools import permutations,product
import fast_triplet as tp
import physic_pc as pc
import physic_pi as pi
import rf_dist_list

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3  
def main(arg1, arg2):              

    with open(arg1) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    t2=Tree(content[0])
    ###print(t2)
    triplets=[]
    taxa=[]

    for i in range(0,len(content)): 
        t1=Tree(content[i])
        leaves,triplets=tp.triplet_decompose(t1,triplets)
        t2=Tree(content[i])
        ###print(t2)
        taxa+=leaves
    ###print(triplets)
    triplets_dict=defaultdict(list)

    for t in triplets:

        trip_key=[t[1][0],t[1][1],t[0]]
        trip_key.sort()
        
        trip_key=str(trip_key).strip('[]')
        trip_key=trip_key.replace("'", '')
        trip_key=trip_key.replace(" ", "")
        
        if (t in triplets_dict[trip_key]) is False :
            triplets_dict[trip_key].append(t)
    ###print(triplets_dict)
    Cpc=pc.physic_pc(list(set(taxa)),triplets,triplets_dict)
    #print(Cpc)
    '''Super_triplet=[]
    #t2=content[0]
    Super_leaves,Supers_triplets=tp.triplet_decompose(Cpc,Super_triplet) 
    R_pi=intersection(triplets,Super_triplet)
    print(R_pi)
    final_tree=pi.check_pi(Cpc,R_pi)
    #print("final is:          --",final_tree)'''
    return Cpc
    
#main("test1.txt",2)                 
