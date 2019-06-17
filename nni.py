from ete3 import Tree,TreeStyle
from itertools import combinations
from collections import defaultdict

def main(arg1, arg2):              
 
    t1=arg1
    counter=0
    Trees_found=[]
    Trees_found.append(t1.write(format=9))
    for node in t1.traverse("preorder"):
        
        if (node.is_leaf() is False) and (node.is_root() is False) :
            node.add_features(count=counter)
            counter+=1
    for i in range(0, counter):
        t2=t1.copy()
        #print(t1) 
        node=t2.search_nodes(count=i)[0]
        #print(node)
        A,B=node.get_children()
        #print(A)
        #print(B)
        pair_node=node.up 
        node.detach() 
        
        #print("------------------------after detachment------------------")
        # print(t2)
        #print(pair_node)
        if not pair_node.up:
            pair_node=pair_node.get_children()[0]
        pair_children= pair_node.get_children()
        if (len(pair_children)==0):
            continue
        C=pair_children[0]
        if len(pair_children)==2:
            #print("-----------------part of pair-----------------")
            
            D=pair_children[1]
        else:
        #D=pair_children[1]
            
            
            node=pair_node.up 
            pair_node.detach()
            node.delete() 
            D=t2
            '''
            print(t1)
            print("A:",A)
            print("B: ",B)
            print("C :",C)
            print("D:",D) 
            '''
           
        nodes=[A,B,C,D]
        nodes_adjust=[]
        for n in nodes:
            if (n.is_leaf() is False):
                #print("!!Checking??????????????????????????!!!")
                
                n_child=n.get_children()
                #print(n_child)
                if len(n_child)==1:
                    #print("it is true!!!!!!!!!!!!!!!!!!!!111 fix me!!!!")
                    #print(n)
                    n=n_child[0]
                    nodes_adjust.append(n)
                else:
                    nodes_adjust.append(n)
            else: nodes_adjust.append(n)
        A=nodes_adjust[0]
        B=nodes_adjust[1]   
        C=nodes_adjust[2]
        D=nodes_adjust[3]
        
        New_tree1=Tree()
        
        First_node=New_tree1.add_child()
        First_node.add_child(A)
        First_node.add_child(C)
        Secnd_node=New_tree1.add_child()
        Secnd_node.add_child(B)
        Secnd_node.add_child(D)
        
        '''print("A:",A)
        print("B: ",B)
        print("C :",C)
        print("D:",D) 
        #print(t1)'''
        #print("New tree1",New_tree1)
        Trees_found.append(New_tree1.write(format=9))
        t2=t1 
        New_tree2=Tree()
        First_node=New_tree2.add_child()
        First_node.add_child(A)
        First_node.add_child(D)
        Secnd_node=New_tree2.add_child()
        Secnd_node.add_child(B)
        Secnd_node.add_child(C)
        Trees_found.append(New_tree2.write(format=9)) 
        #print(t1)
        #print("New tree2",New_tree2)
        t2=t1  
               
    return Trees_found   
        
    
#main("test1.txt",2)