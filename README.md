# Biological Applications of Random Walk with Restart on Multilayer Networks
Anthony Baptista, Galadriel Brière, Anaïs Baudot

## Node prioritization in Leukemia

<div style="max-width:100%;"><img src="Leukemia/multiXrank_results/cytoscape_net/top20.png" alt="Top 20 genes and drugs prioritized in Leukemia"></div>

### Run MultiXrank using the following command line:

```python ~/ApplicationsMultiXrank/Leukemia/script_bash.py``` 

### Visualize results
Visualize top 20 proritized genes and drugs in Cytoscape with file: [Leukemia/multiXrank_results/cytoscape_net/top20.cys](Leukemia/multiXrank_results/cytoscape_net/top20.cys)

Or explore the network on your browser: [Leukemia/multiXrank_results/cytoscape_net/web_session](Leukemia/multiXrank_results/cytoscape_net/web_session/)

## Node prioritization in Epilepsy using the Hetionet framework

### Learn more about Hetionet 

+ [**Systematic integration of biomedical knowledge prioritizes drugs for repurposing**](https://doi.org/10.7554/eLife.26726)<br>
  Daniel S Himmelstein, Antoine Lizee, Christine Hessler, Leo Brueggeman, Sabrina L Chen, Dexter Hadley, Ari Green, Pouya Khankhanian, Sergio E Baranzini<br>
  _eLife_. 2017. DOI: 10.7554/eLife.26726

### Run MultiXrank using the following command line:

#### Build Hetionet network
```python ~/ApplicationsMultiXrank/Epilepsy/HetionetDB_to_MultiXrankDB/hetionet_to_multixrank.py``` 

#### Run MultiXrank
```python ~/ApplicationsMultiXrank/Epilepsy/script_bash.py``` 

#### Run downstream analysis of MultiXrank scores
```python ~/ApplicationsMultiXrank/Epilepsy/downstream_analysis/give_name.py``` 
```python ~/ApplicationsMultiXrank/Epilepsy/downstream_analysis/check_results.py``` 
```python ~/ApplicationsMultiXrank/Epilepsy/downstream_analysis/code_pie_tot.py``` 