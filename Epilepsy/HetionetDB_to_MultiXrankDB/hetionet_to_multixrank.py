#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

# Out directories for multiplex and bipartite networks
out_path_multi = "../multiplex/"
os.makedirs(out_path_multi, exist_ok=True)
for i in range(1, 10):
    directory = out_path_multi + str(i)
    os.makedirs(directory, exist_ok=True)

out_path_bipartite = "../bipartite/"
os.makedirs(out_path_bipartite, exist_ok=True)

# Read Hetionet nodes and edges files
hetionet_edges =  pd.read_csv("HetionetDB/hetionet-v1.0-edges.sif", sep = '\t')
hetionet_nodes =  pd.read_csv("HetionetDB/hetionet-v1.0-nodes.tsv", sep = '\t')

#### Multiplex 1: Gene multiplex (GcG, GiG, GrG)
hetionet_genes = hetionet_nodes[hetionet_nodes["kind"] == "Gene"]["id"]
gene_GcG = hetionet_edges[hetionet_edges["metaedge"] == "GcG"].drop("metaedge", axis=1)
gene_GiG = hetionet_edges[hetionet_edges["metaedge"] == "GiG"].drop("metaedge", axis=1)
gene_GrG = hetionet_edges[hetionet_edges["metaedge"] == "Gr>G"].drop("metaedge", axis=1)

# Check every gene is connected in each layer, else add self loop
all_GcG_genes = pd.concat([gene_GcG['source'],gene_GcG['target']]).drop_duplicates()
unmapped_GcG_genes = hetionet_genes[~hetionet_genes.isin(all_GcG_genes)] 
self_GcG = pd.DataFrame({'source': unmapped_GcG_genes, 'target': unmapped_GcG_genes})
full_GcG = pd.concat([self_GcG, gene_GcG])

all_GiG_genes = pd.concat([gene_GiG['source'],gene_GiG['target']]).drop_duplicates()
unmapped_GiG_genes = hetionet_genes[~hetionet_genes.isin(all_GiG_genes)] 
self_GiG = pd.DataFrame({'source': unmapped_GiG_genes, 'target': unmapped_GiG_genes})
full_GiG = pd.concat([self_GiG, gene_GiG])

all_GrG_genes = pd.concat([gene_GrG['source'],gene_GrG['target']]).drop_duplicates()
unmapped_GrG_genes = hetionet_genes[~hetionet_genes.isin(all_GrG_genes)] 
self_GrG = pd.DataFrame({'source': unmapped_GrG_genes, 'target': unmapped_GrG_genes})
full_GrG = pd.concat([self_GrG, gene_GrG])

# Write resuls
full_GcG.to_csv(out_path_multi+"/1/GcG.tsv", sep = '\t', header = None, index = False)
full_GiG.to_csv(out_path_multi+"/1/GiG.tsv", sep = '\t', header = None, index = False)
full_GrG.to_csv(out_path_multi+"/1/GrG.tsv", sep = '\t', header = None, index = False)

#### Multiplex 2: Disease monoplex (DrD)
hetionet_diseases = hetionet_nodes[hetionet_nodes["kind"] == "Disease"]["id"]
disease_DrD = hetionet_edges[hetionet_edges["metaedge"] == "DrD"].drop("metaedge", axis=1)
# Check every disease is connected in the layer, else add self loop
all_diseases = pd.concat([disease_DrD['source'],disease_DrD['target']]).drop_duplicates()
unmapped_diseases = hetionet_diseases[~hetionet_diseases.isin(all_diseases)] 
self_DrD = pd.DataFrame({'source': unmapped_diseases, 'target': unmapped_diseases})
full_DrD = pd.concat([self_DrD, disease_DrD])
full_DrD.to_csv(out_path_multi+"/2/DrD.tsv", sep = '\t', header = None, index = False)

#### Multiplex 3: Compound monoplex (CrC)
hetionet_compounds = hetionet_nodes[hetionet_nodes["kind"] == "Compound"]["id"]
compound_CrC = hetionet_edges[hetionet_edges["metaedge"] == "CrC"].drop("metaedge", axis=1)
# Check every compound is connected in the layer, else add self loop
all_compounds = pd.concat([compound_CrC['source'],compound_CrC['target']]).drop_duplicates()
unmapped_compounds = hetionet_compounds[~hetionet_compounds.isin(all_compounds)] 
self_CrC = pd.DataFrame({'source': unmapped_compounds, 'target': unmapped_compounds})
full_CrC = pd.concat([self_CrC, compound_CrC])
full_CrC.to_csv(out_path_multi+"/3/CrC.tsv", sep = '\t', header = None, index = False)


#### Multiplex 4: Anatomy monoplex (self loops)
# For this layer, we don't have any relation -> Add self loops.
hetionet_anatomy = hetionet_nodes[hetionet_nodes["kind"] == "Anatomy"]["id"]
full_AselfA =  pd.DataFrame({'source': hetionet_anatomy, 'target': hetionet_anatomy})
full_AselfA.to_csv(out_path_multi+"/4/AselfA.tsv", sep = '\t', header = None, index = False)

#### Multiplex 5: Symptom monoplex (self loops)
# For this layer, we don't have any relation -> Add self loops.
hetionet_symptom = hetionet_nodes[hetionet_nodes["kind"] == "Symptom"]["id"]
full_SselfS =  pd.DataFrame({'source': hetionet_symptom, 'target': hetionet_symptom})
full_SselfS.to_csv(out_path_multi+"/5/SselfS.tsv", sep = '\t', header = None, index = False)

#### Multiplex 6: Side Effecs monoplex (self loops)
hetionet_side = hetionet_nodes[hetionet_nodes["kind"] == "Side Effect"]["id"]
full_SEselfSE =  pd.DataFrame({'source': hetionet_side, 'target': hetionet_side})
full_SEselfSE.to_csv(out_path_multi+"/6/SEselfSE.tsv", sep = '\t', header = None, index = False)

#### Multiplex 7: Pharmacologic Class (self loops)
hetionet_pharm = hetionet_nodes[hetionet_nodes["kind"] == "Pharmacologic Class"]["id"]
full_PCselfPC =  pd.DataFrame({'source': hetionet_pharm, 'target': hetionet_pharm})
full_PCselfPC.to_csv(out_path_multi+"/7/PCselfPC.tsv", sep = '\t', header = None, index = False)

#### Multiplex 8: Pathway monoplex (self loops)
hetionet_pathway = hetionet_nodes[hetionet_nodes["kind"] == "Pathway"]["id"]
full_PselfP =  pd.DataFrame({'source': hetionet_pathway, 'target': hetionet_pathway})
full_PselfP.to_csv(out_path_multi+"/8/PWselfPW.tsv", sep = '\t', header = None, index = False)

#### Multiplex 9: Gene Ontology multiplex (GO:BP self loops, GO:MF self loops, GO:CC self loops)
hetionet_BP = hetionet_nodes[hetionet_nodes["kind"] == "Biological Process"]["id"]
full_BPselfBP =  pd.DataFrame({'source': hetionet_BP, 'target': hetionet_BP})

hetionet_CC = hetionet_nodes[hetionet_nodes["kind"] == "Cellular Component"]["id"]
full_CCselfCC =  pd.DataFrame({'source': hetionet_CC, 'target': hetionet_CC})

hetionet_MF = hetionet_nodes[hetionet_nodes["kind"] == "Molecular Function"]["id"]
full_MFselfMF =  pd.DataFrame({'source': hetionet_MF, 'target': hetionet_MF})

full_GO = pd.concat([full_BPselfBP, full_CCselfCC, full_MFselfMF])
full_GO.to_csv(out_path_multi+"/9/GOselfGO.tsv", sep = '\t', header = None, index = False)

#### Bipartite 1-8: Gene - Pathway (GpPW)
gene_pathway_GpPW = hetionet_edges[hetionet_edges["metaedge"] == "GpPW"].drop("metaedge", axis=1)
gene_pathway_GpPW.to_csv(out_path_bipartite+"/1_8.tsv", sep = '\t', header = None, index = False)

#### Bipartite 1-9:  Gene - GO (GpBP, GpMF, GpCC)
gene_GO_GpBP = hetionet_edges[hetionet_edges["metaedge"] == "GpBP"].drop("metaedge", axis=1)
gene_GO_GpCC = hetionet_edges[hetionet_edges["metaedge"] == "GpCC"].drop("metaedge", axis=1)
gene_GO_GpMF = hetionet_edges[hetionet_edges["metaedge"] == "GpMF"].drop("metaedge", axis=1)
full_gene_GO = pd.concat([gene_GO_GpBP, gene_GO_GpCC, gene_GO_GpMF]) 
full_gene_GO.to_csv(out_path_bipartite+"/1_9.tsv", sep = '\t', header = None, index = False)

#### Bipartite 2-1: Disease - Gene (DaG, DuG, DdG)
gene_disease_DaG = hetionet_edges[hetionet_edges["metaedge"] == "DaG"].drop("metaedge", axis=1)
gene_disease_DuG = hetionet_edges[hetionet_edges["metaedge"] == "DuG"].drop("metaedge", axis=1)
gene_disease_DdG = hetionet_edges[hetionet_edges["metaedge"] == "DdG"].drop("metaedge", axis=1)
# Drop duplicates
full_gene_disease = pd.concat([gene_disease_DaG, gene_disease_DuG, gene_disease_DdG]).drop_duplicates() 
full_gene_disease.to_csv(out_path_bipartite+"/2_1.tsv", sep = '\t', header = None, index = False)

#### Bipartite 2-4: Disease - Anatomy (DlA)
disease_anatomy = hetionet_edges[hetionet_edges["metaedge"] == "DlA"].drop("metaedge", axis=1)
disease_anatomy.to_csv(out_path_bipartite+"/2_4.tsv", sep = '\t', header = None, index = False)

#### Bipartite 2-5: Disease - Symptom (DpS)
disease_symptom = hetionet_edges[hetionet_edges["metaedge"] == "DpS"].drop("metaedge", axis=1)
disease_symptom.to_csv(out_path_bipartite+"/2_5.tsv", sep = '\t', header = None, index = False)

#### Bipartite 3-1: Compound - Gene (CuG, CbG, CdG)
gene_compound_CuG = hetionet_edges[hetionet_edges["metaedge"] == "CuG"].drop("metaedge", axis=1)
gene_compound_CbG = hetionet_edges[hetionet_edges["metaedge"] == "CbG"].drop("metaedge", axis=1)
gene_compound_CdG = hetionet_edges[hetionet_edges["metaedge"] == "CdG"].drop("metaedge", axis=1)
# Drop duplicates
full_gene_compound = pd.concat([gene_compound_CuG, gene_compound_CbG, gene_compound_CdG]).drop_duplicates() 
full_gene_compound.to_csv(out_path_bipartite+"/3_1.tsv", sep = '\t', header = None, index = False)

#### Bipartite 3-2: Compound - Disease (CtD, CpD)
compound_disease_CtD = hetionet_edges[hetionet_edges["metaedge"] == "CtD"].drop("metaedge", axis=1)
compound_disease_CpD = hetionet_edges[hetionet_edges["metaedge"] == "CpD"].drop("metaedge", axis=1)
# Drop duplicates
full_compound_disease = pd.concat([compound_disease_CtD, compound_disease_CpD]).drop_duplicates() 
full_compound_disease.to_csv(out_path_bipartite+"/3_2.tsv", sep = '\t', header = None, index = False)

#### Bipartite 3-6: Compound - Side Effect (CcSE)
compound_SE = hetionet_edges[hetionet_edges["metaedge"] == "CcSE"].drop("metaedge", axis=1)
compound_SE.to_csv(out_path_bipartite+"/3_6.tsv", sep = '\t', header = None, index = False)

#### Bipartite 4-1: Anatomy - Gene (AdG, AuG, AeG)
anatomy_gene_AdG = hetionet_edges[hetionet_edges["metaedge"] == "AdG"].drop("metaedge", axis=1)
anatomy_gene_AuG = hetionet_edges[hetionet_edges["metaedge"] == "AuG"].drop("metaedge", axis=1)
anatomy_gene_AeG = hetionet_edges[hetionet_edges["metaedge"] == "AeG"].drop("metaedge", axis=1)
# Drop duplicates
full_antomy_gene = pd.concat([anatomy_gene_AdG, anatomy_gene_AuG, anatomy_gene_AeG]).drop_duplicates() 
full_antomy_gene.to_csv(out_path_bipartite+"/4_1.tsv", sep = '\t', header = None, index = False)

#### Bipartite 7-3: Pharmacologic Class - Compound (PCiC)
pharmaco_compound = hetionet_edges[hetionet_edges["metaedge"] == "PCiC"].drop("metaedge", axis=1)
pharmaco_compound.to_csv(out_path_bipartite+"/7_3.tsv", sep = '\t', header = None, index = False)

