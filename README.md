# Biological Applications of Random Walk with Restart on Multilayer Networks
Anthony Baptista, Galadriel Brière, Anaïs Baudot

## Node prioritization in Leukemia

<div style="max-width:100%;"><img src="Leukemia/multiXrank_results/cytoscape_net/top20.png" alt="Top 20 genes and drugs prioritized in Leukemia"></div>

### Run MultiXrank using the following command line:

```python ~/ApplicationsMultiXrank/Leukemia/script_bash.py``` 

### Visualize results
Visualize top 20 proritized genes and drugs in Cytoscape with file: [Leukemia/multiXrank_results/cytoscape_net/top20.cys](Leukemia/multiXrank_results/cytoscape_net/top20.cys)

Or explore the network on your browser: [Leukemia/multiXrank_results/cytoscape_net/web_session](Leukemia/multiXrank_results/cytoscape_net/web_session/)

## Node prioritization in Epilepsy and Nicotine Dependence using the Hetionet framework

### Learn more about Hetionet 

+ [**Systematic integration of biomedical knowledge prioritizes drugs for repurposing**](https://doi.org/10.7554/eLife.26726)<br>
  Daniel S Himmelstein, Antoine Lizee, Christine Hessler, Leo Brueggeman, Sabrina L Chen, Dexter Hadley, Ari Green, Pouya Khankhanian, Sergio E Baranzini<br>
  _eLife_. 2017. DOI: 10.7554/eLife.26726

### Run MultiXrank using the following command line:

#### Build Hetionet network
```python ~/ApplicationsMultiXrank/Hetionet/HetionetDB_to_MultiXrankDB/hetionet_to_multixrank.py``` 

#### Run MultiXrank
##### Epilepsy
```python ~/ApplicationsMultiXrank/Hetionet/Epilepsy/script_bash.py``` 

##### Nicotine Dependence
```python ~/ApplicationsMultiXrank/Hetionet/NicotineDependence/script_bash.py``` 


#### Run downstream analysis of MultiXrank scores
##### Epilepsy
```python ~/ApplicationsMultiXrank/Hetionet/Epilepsy/downstream_analysis/give_name.py``` 

```python ~/ApplicationsMultiXrank/Hetionet/Epilepsy/downstream_analysis/check_results.py```

```python ~/ApplicationsMultiXrank/Hetionet/Epilepsy/downstream_analysis/code_pie_tot.py``` 

##### Nicotine Dependence
```python ~/ApplicationsMultiXrank/Hetionet/NicotineDependence/downstream_analysis/give_name.py``` 

## Suppervised prediction of gene-disease associations

### Create the training set 
#### 1914 positive G-D associations (from DisGeNET v2.0) and 1914 negative G-D associations
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/training_set.py``` 

### Running MXR for all associations in the training set
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/generate_rwr.py```

### Store MXR results in sparse matrices
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/make_sparse_matrices.py```

### Train classifiers
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/train_models.py```

### Compare DisGeNET v2.0 (2014) and DisGeNET v7.0 (2020) associations
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/test_2020associations/compare_2014_2020_associations.py```

### Generate test set
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/test_2020associations/make_test_set.py```

### Run MXR for the test set
```python ~/ApplicationsMultiXrank/GeneDiseaseAssociations/1_gene_disease_multiplexes/test_2020associations/generate_rwr.py```



