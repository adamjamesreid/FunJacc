# FunJacc
Summarising functional enrichment terms using clustering

Here I am developing code to summarise goProfiler output using Jaccard similarity of term-associated gene lists and clustering

# Cluster using all terms types
python3  funjacc.py -g KD_in_High_go_terms_res.txt -d GO:BP,GO:MF,GO:CC,CORUM,KEGG,HPA,REAC,WP,TF
python3  funjacc.py -g KD_in_Low_go_terms_res.txt -d GO:BP,GO:MF,GO:CC,CORUM,KEGG,HPA,REAC,WP,TF
