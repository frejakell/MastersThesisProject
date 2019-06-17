
from ete3 import Tree,TreeStyle
from itertools import combinations
def list_def(l_trips,list1, list2):
    #print(list1)
    #print(list2)
    #print(list3)
    gs=list(combinations(list1, 2))
    list_full=[]
    for ele in gs:
        for leaf in list2:
            
            
            temp=ele
            
            temp=temp+(leaf,)
            
            list_full.append(tuple(sorted(temp)))
    #print(list_full)
    #print(l_trips)
    l_trips=set(l_trips)-set(list_full)
           
    return(l_trips)
def bulid_list(list1, list2, trips_list):
    
    for x in list1:
        for y in list2:
            if [x,sorted(y)] not in trips_list:
                trips_list.append([x,sorted(y)])
    return trips_list
def prepostorder(self):
        _leaf = self.__class__.is_leaf
        to_visit = [self]
        

        while to_visit:
            node = to_visit.pop(-1)
            try:
                node = node[1]
            except TypeError:
              
                yield (False, node)
                if not _leaf(node):
                   
                    to_visit.extend(reversed(node.children + [[1, node]]))
            else:
           
                yield (True, node)
                
                
                
def path_from_root_to_node(t):
    d_node=dict()
    d_children=dict()
    edge = 0
    for node in t.traverse():
       if not node.is_leaf():
          node.name = edge
          edge += 1


    current_path = [t]
    for postorder, node in prepostorder(t):
        
        
        if postorder:
            
            current_path.pop(-1)
        else:
            if not node.children:
                
                
                d_node[node.name]=[]
                d_children[node.name]=[]
               
                for i in range(1,len(current_path)):  
              
                 
                    if current_path[i] !=0:
                        d_node[node.name].append(current_path[i])
                pass
                
            else:
                current_path.append(node.name)
                d_children[node.name]=[node.children[0].name,node.children[1].name]
    return d_node,d_children
def descendant_iterator(node, d_children, subtree):
    
    if len(d_children[node])!=0:
       
       for child in d_children[node]:
            if(isinteger(child)==False and child is not "[...]"):
                subtree.append(child)
                
            else:
                subtree=descendant_iterator(child, d_children, subtree)
    return subtree
    
def isinteger(a):
    try:
        int(a)
        return True
    except ValueError:
        return False
def main(arg1,triplets):              

    s1 = str(arg1)
    #s1 = str(arg2)
    shared=0
    d_node=dict()
    d_path=dict()
    d_children=dict()
    t1 = Tree(s1)
    #t2 = Tree(s2)
    L=[]
    trips=[]
    for leaf in t1:
        L.append(leaf.name)
    L=sorted(L)
    all_comb=list(combinations(L,3))
    #print(all_comb)
    trips=all_comb
    d_node,d_children=path_from_root_to_node(t1)
    #d_node2,d_children2=path_from_root_to_node(t2)
    
  
   
    d_node,d_children=path_from_root_to_node(t1)
    #d_node2,d_children2=path_from_root_to_node(t2)
    trips=[]
    Red=[]
    Blue=[]
    #print(t1)
    for node in t1.traverse("levelorder"):
         if not node.is_leaf():
            subtree1=[]
            subtree2=[]
            children=d_children[node.name]
            if(isinteger(children[0])==False):
                subtree1.append(children[0])
               
            if(isinteger(children[1])==False):
                subtree2.append(children[1])
                
            subtree1=descendant_iterator(children[0],d_children,subtree1)
            subtree2=descendant_iterator(children[1],d_children,subtree2)
 
            red=subtree1
            blue=subtree2
            #print(red)
            #print(blue)
            sub_red2= list(combinations(red,2))
            sub_blue2=list(combinations(blue,2))
            #print(sub_red2)
            #print(sub_blue2)
            #print("--------------------------------------------")
            triplets=bulid_list(red, sub_blue2,triplets)
            #[[x,y] for x in red for y in sub_blue2]
            triplets=bulid_list(blue, sub_red2,triplets)
            #trips=trips+[[x,y] for x in blue for y in sub_red2]
            #sub1_red= len( list(combinations(red,2)))
            #sub1_blue= len( list(combinations(blue,2)))
            
    #print(trips)
    return L,triplets


if __name__ == '__main__':
    s1="(ab, (ad, ((af, (aa, ac)), ae)));"

    s2="(((ad, ab), aa), ((af, ae), ac));"
    triplets=[]
    l,tri=main(s1,triplets)
    print(tri)
    