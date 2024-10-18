# FunJacc
Summarising functional enrichment terms using clustering

Here I am developing code to summarise gProfiler output using Jaccard similarity of term-associated gene lists and clustering

This is still very much under development!!!

## Usage

Prerequisites:

- Conda/Mamba
- Git

**Clone Git repository**

`git clone https://github.com/adamjamesreid/FunJacc.git`

`cd FunJacc`

**Setup mamba environment**

`mamba env create -f funjacc.yaml -n funjacc`

`mamba activate funjacc`

**Execute snakemake pipeline**

Your input file should be in a directory called 'input' and be named '{string}.list'. The {string} can be anything you like.

To run snakemake you need to specify the final output file, so here we arbitrarily pick one of them, which will be the file of cluster annotation, found in a new directory called 'funjacc_res'. It will be named with the {string} used in your input file, so here, replace {string} with the same characters that are before '.list' in your input file

`snakemake funjacc_res/{string}.ann.txt`

**Output**

./gprofiler/{string}.gprofiler.out - Initial output from Gprofiler

./funjacc_res/{string}.ann.txt - Cluster annotations, which can be read into Cytoscape
./funjacc_res/{string}.gprofiler.tsv - Gprofiler output, annotated with FunJacc cluster numbers and names
./funjacc_res/{string}.ntwrk.txt - FunJacc network file which can be read into Cytoscape
./funjacc_res/{string}.ntwrk.txtdata.mci - MCL output file
./funjacc_res/{string}.ntwrk.txtdata.mci.inf1.4 - MCL output file
./funjacc_res/{string}.ntwrk.txtdata.mci.inf1.4.clusters.txt - MCL output file
./funjacc_res/{string}.ntwrk.txt.data.tab - MCL output file

## Old usage

**Run gprofiler**

`Rscript run_gprofiler.R test.list test.out hsapiens`

**Cluster using all terms types**

`python3  funjacc.py -g test.out -d GO:BP,GO:MF,GO:CC,CORUM,KEGG,REAC,WP,TF`

**Visualising in Cytoscape**

The Cytoscape style file allows the metadata provided by FunJacc to be used to annotate the network

The *ntwk* output file describes the network, the *ann* file describes the node attributes
