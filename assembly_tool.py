import TMC
import GSCM
import Build 
import SF
import PhySIC
from ete3 import Tree,TreeStyle

ans=True  
print ("""
       -------------------------------------------------------------------------
       /////////////////////////////////////////////////////////////////////////
       -------------------------------------------------------------------------
                            SuperTree Assembly
        -------------------------------------------------------------------------
       /////////////////////////////////////////////////////////////////////////
       -------------------------------------------------------------------------
       Options:
           -h, --help show this help message
           -e, --exit
      Input options:
            -s SOURCE, 
                Filename for source trees in newick format(required)
            -m [Method/Methods], 
                list of methods to compute the supertree on (required)
                -GSCM
                -Build
                -TM: Triplet MaxCut
                -SF: SuperFine +Triple MaxCut 
            -t TrueTree
                the Filename for the true tree in newick format(optional)

      Output options:
            -ps print to screen
            -pf OutPutFile(optional) 
                print to File specifed 
            -sc Score Supertrees 
            -rf(optional)  
                construct robinson-fould distance matrix between the outputed trees""")
while ans:

    ans=input("What would you like to do? ") 
    if ans=="-h": 
          print ("""
       -------------------------------------------------------------------------
       /////////////////////////////////////////////////////////////////////////
       -------------------------------------------------------------------------
                            SuperTree Assembly
        -------------------------------------------------------------------------
       /////////////////////////////////////////////////////////////////////////
       -------------------------------------------------------------------------
       Options:
           -h, --help show this help message
           -e, --exit
      Input options:
            -s SOURCE, 
                Filename for source trees in newick format(required)
            -m [Method/Methods], 
                list of methods to compute the supertree on (required)
                -GSCM
                -Build
                -TM: Triplet MaxCut
                -SF: SuperFine +Triple MaxCut 
            -t TrueTree
                the Filename for the true tree in newick format(optional)

      Output options:
            -ps print to screen
            -pf OutPutFile(optional) 
                print to File specifed 
            -sc Score Supertrees 
            -rf(optional)  
                construct robinson-fould distance matrix between the outputed trees"""
                
            ) 
    elif ans=="-e":
        print("\n Goodbye") 
        ans=False 
    elif ('-s' not in ans) or ('-m' not in ans):
        print("\n input error, sounce and method are mandatory") 
    else:
        words = ans.split()
        print(words) 
        methods=ans[ans.find("[")+1:ans.find("]")] 
       
        index = words.index('-s')
        file_name=words[index+1]
        with open(file_name) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content] 
        index = words.index('-m')
        methods=methods.split(',') 
        
        print(methods)
        trees={}
        
        if(("SF" in methods)or (" SF" in methods)):
            trees_structure,overlap_per,inconsist_per=SF.main(file_name,2)
            trees["SuperFine"]=trees_structure
            #print(trees_structure)
            #trees_structure.show()
        if("Build" in methods):
            tree_Build=Build.main(file_name,1)
            trees["Build"]=tree_Build
        if("GSCM" in methods):
            tree_scm=GSCM.main(file_name,"Common")
            trees["GSCM"]=tree_scm
            #tree_scm.show()
        if("TMC" in methods):
            tree_TMC,overlap_per1,inconsist_per1,triplets_dict1=TMC.main(file_name,2)
            trees["Triplet MaxCut"]=tree_TMC
            #tree_TMC.show()
        if("PhySIC" in methods):
            tree_PhySIC=PhySIC.main(file_name,1)
            trees["PhySIC"]=tree_PhySIC
            #tree_PhySIC.show()
        
        if("-ps"in ans):
            for keys in trees:
                t1=trees[keys]
                t1.show()
        print(trees)       
        if("-pf"in ans):
            index = words.index('-pf')
            file_output=words[index+1]
            f_w = open(file_output, "w") 
            print("output is",file_output)
            for keys in trees:
                t1=trees[keys]
                f_w.write(keys +":  "+t1.write(format=9)+"\n")
                
        if("-sc"in ans):
            if("-t"in ans):
                index_tt = words.index('-t')
                index_tt=words[index_tt+1]
                with open(index_tt) as f:
                    tt = f.readlines()
                tt = [x.strip() for x in tt] 
                t2=Tree(tt[0])
                for keys in trees:
                    t1=trees[keys]
                    rf= t1.robinson_foulds(t2)
                    max_distance=rf[1]
                    False_branch= len(rf[3]-rf[4])+len(rf[4]-rf[3])
                    Tp= max_distance-False_branch
                    score_F1= 2*Tp/(2*Tp+False_branch)
                    print(keys +" F1 Score: "+ str(score_F1))
            else:
                print("RF distance Score")
                for keys in trees:
                    t2=trees[keys]
                    incorrect=0
                    missing=0
                    RF=0
                    total=0
                    for i in range(0,len(content)): 
                       
                        t1=Tree(content[i])
                        rf = t1.robinson_foulds(t2)
                        incorrect +=len(rf[3]-rf[4])
                        missing +=len(rf[4]-rf[3])
                        RF+=rf[0]
                        total+=rf[1]
                        
                    
                    RF_normal=RF/total
                    print(keys +": "+ str(RF_normal))    