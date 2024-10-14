# FunJacc
Summarising functional enrichment terms using clustering

Here I am developing code to summarise goProfiler output using Jaccard similarity of term-associated gene lists and clustering

# Run gprofiler
Rscript run_gprofiler.R test.list test.out hsapiens
# Cluster using all terms types
python3  funjacc.py -g test.out -d GO:BP,GO:MF,GO:CC,CORUM,KEGG,REAC,WP,TF
