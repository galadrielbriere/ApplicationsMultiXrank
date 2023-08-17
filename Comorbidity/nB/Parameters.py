import numpy as np

## Random walk parameters :
#1. Global Restart Probability (r) 
r = 0.7
#2. Inter-Layer Jump Probability (delta) 
delta = np.array([1/2,0,0,0])
#3. Layers Restart Probability (tau)
tau = np.array([[1/3,1/3,1/3],\
                [1,0,0],\
                [1,0,0],\
                [1,0,0]])
#4. Inter Network Jump Probability (lambda)
lamb = np.array([[1/4,1/4,1/4,1/4],\
                 [1/4,1/4,1/4,1/4],\
                 [1/4,1/4,1/4,1/4],\
                 [1/4,1/4,1/4,1/4]])
#5. Networks Restart Probability (eta)
eta = np.array([0,0,0,1])
#6. Number of Top Genes to be included in the output network (K)
K = 'all'

## system strusture parameters :
# Name of layers of each multiplex (key name)
Multiplex1 = ["PPI","Reactome","Complexes"]
Multiplex2 = ["nB"]
Multiplex3 = ["tad"]
Multiplex4 = ["disease"]
Multilayer = [Multiplex1, Multiplex2, Multiplex3, Multiplex4]
# Name of nodes in each multiplex
Multiplex1_nodes = ["protein1", "protein2"]
Multiplex2_nodes = ["fragment1", "fragment2"]
Multiplex3_nodes = ["tad1", "tad2"]
Multiplex4_nodes = ["disease1", "disease2"]
Multilayer_nodes = [Multiplex1_nodes, Multiplex2_nodes, Multiplex3_nodes, Multiplex4_nodes]
# Kind of interactions in each layer of each multiplex
Multiplex1_interactions = ['00', '00', '00']
Multiplex2_interactions = ['10']
Multiplex3_interactions = ['00']
Multiplex4_interactions = ['00']
Multilayer_interactions = [Multiplex1_interactions, Multiplex2_interactions, Multiplex3_interactions, Multiplex4_interactions]
# Kind of interactions in each bipartite
Bipartite_interactions = [[0, '00', 0, 0],
                          [0, 0, 0, 0],
                          ['00', '00', 0, 0],
                          ['10', 0, 0, 0]]
