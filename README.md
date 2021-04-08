# MastersThesisProject

The code in this repository contains the assembly of supertree algortihms implemented for my Master thesis project (Aarhus University, 2019)

The project consists of a number of different SuperTree algorithms: 
  1. PluMist algorithm
  2. Triplet MaxCut algorithm
  3. PhySIC algorithm
  4. FlipCut algorithm
  5. Greedy strict consensus merger algorithm
  6. Build algorithm


The code includes an assembly program (assembly_tool.py) that makes the project more user friendly. If you run this program you will see the following menu:

       --------------------------------------------------------------------------
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
                
                
