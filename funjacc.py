# Given a set of GO terms results, determine the Jaccard index between the sets of e.g. DE genes associated with each term
# output results so a network can be drawn and or representative terms could be picked.

# AUTHOR: Adam James Reid
# Copyright (C) 2024 University of Cambridge
# This program is distributed under the terms of the GNU General Public License

import sys
import subprocess
import argparse

# Default options
p_cut = 1e-5
jaccard_cut = 0.5 # Jaccard score above which to report a network edge
data_types = ['GO:BP']
inflation = 2

default_node_label_size = 5
cluster_label_size = 20

# Colour for annotating clusters
colours = ['#FFC312','#C4E538','#12CBC4','#FDA7DF','#ED4C67',
  '#F79F1F','#A3CB38','#1289A7','#D980FA','#B53471',
  '#EE5A24','#009432','#0652DD','#9980FA','#833471',
  '#EA2027','#006266','#1B1464','#5758BB','#6F1E51'
  '#40407a','#706fd3','#f7f1e3','#34ace0','#33d9b2',
  '#2c2c54','#474787','#aaa69d','#227093','#218c74',
  '#ff5252','#ff793f','#d1ccc0','#ffb142','#ffda79',
  '#b33939','#cd6133','#84817a','#cc8e35','#ccae62']
default_colour = '#FDE725FF' # For if we run out of colours

# Argument parser
parser = argparse.ArgumentParser(description="go_term_sim_network v1.1 - Cluster gProfiler GO term results based on associated genes, Adam Reid (ajr236@cam.ac.uk)")
parser.add_argument("-p", type=float, help="P-value cutoff for GO term enrichment [0.01]", default=0.01)
parser.add_argument("-j", type=float, help="Jaccard coefficient above which to report a network edge", default=0.5)
parser.add_argument("-d", type=str, help="Comma-separated list of data types to include e.g. GO:BP,GO:MF,GO:CC,CORUM", default='GO:BP')
parser.add_argument("-I", type=float, help="Inflation parameter for MCL clustering")
parser.add_argument("-g", type=str, help="gProfiler term enrichment results")
parser.add_argument("-o", type=str, help="Output directory", default=".")
args = parser.parse_args()

# Assign command line arguments to variables
if(args.d):
    data_types = args.d.split(',')
else:
    data_types = ['GO:BP']
if(args.p):
    p_cut = args.p
if(args.j):
    jaccard_cut = args.j
if(args.I):
    inflation = args.I
if(args.o):
    outdir = args.o

if(args.g):
    data = args.g

# Get core of filename for use in making output names
outstem = data.split('/')[-1].split('.')[0]
# Add outdir to outstem
outstem = outdir + '/' + outstem

# Store names 
term_names = dict()

# Store associated gene names as dictionary of sets
gene_names = dict()
term_types = dict() # Store term type for each term

# Read through results and store genes associated with each significant term
with open(data) as d:
    for x in d.readlines():
        x = x.rstrip()
        v = x.split('\t')
        # Skip header
        if v[0] == 'query':
            continue
        # Include only data types mentioned in data_types
        if v[10] not in data_types:
            continue
        # Exclude terms with high p value
        if float(v[3]) < p_cut:
            #print(v[9], v[11],  v[15])
            term_names[v[9]] = v[11]
            if v[11] not in term_types:
                term_types[v[11]] = set()
            term_types[v[11]].add(v[10])
            if v[9] not in gene_names:
                gene_names[v[9]] = set()

            gene_names[v[9]] = set(v[15].split(','))

            #print(gene_names[v[9]])

# Open output file for writing the network
network_outfile = outstem+'.ntwrk.txt'
ntwrk_out = open(network_outfile, 'w')
# Nectwork file header
ntwrk_out.write("source\ttarget\tjaccard_coeff\n")

# Record which terms which are connected so we can add in those which aren't
connected_terms = set()

for g1 in gene_names:
    for g2 in gene_names:
        inter = gene_names[g1].intersection(gene_names[g2])
        union = gene_names[g1].union(gene_names[g2])
        j = float(len(inter)) / float(len(union))
        if j > 0 and g1 != g2 and j >= jaccard_cut:
            #print("{}\t{}\t{}\t{}\t{}".format(g1, g2, len(inter), len(union), j))
            #print("{}\t{}\t{}".format(term_names[g1], term_names[g2], j))
            ntwrk_out.write("{}\t{}\t{}\n".format(term_names[g1], term_names[g2], j))

            connected_terms.add(g1)
            connected_terms.add(g2)


#Add in unconnected but significant terms
for g in gene_names:
    if g not in connected_terms:
        ntwrk_out.write("{}\t{}\t{}\n".format(term_names[g], term_names[g], 1))

ntwrk_out.close()



# then run MCL pipeline
clusters_outfile_name = network_outfile+'data.mci.inf'+str(inflation)+'.clusters.txt'
subprocess.run(['mcxload', '-abc', network_outfile, '--stream-mirror', '-write-tab', network_outfile+'.data.tab', '-o', network_outfile+'data.mci'])
subprocess.run(['mcl', network_outfile+'data.mci', '-I', str(inflation), '-o', network_outfile+'data.mci.inf'+str(inflation)])
subprocess.run(['mcxdump', '-icl', network_outfile+'data.mci.inf'+str(inflation), '-tabr', network_outfile+'.data.tab', '-o', clusters_outfile_name])

# Then annotate clusters
# Cluster numbering
c = 1

# Print header
ann_outfile = outstem+'.ann.txt'
ann_out = open(ann_outfile, 'w')
print('{}\t{}\t{}'.format("node", "cluster", "cluster_name"))
ann_out.write('term\tcluster_number\tcluster_name\tterm_type\tcolour\tlabel_size\n')

# Save cluster details here for writing to gProfiler output
term_to_cluster = dict()

with open(clusters_outfile_name) as df:
    for x in df.readlines():
        x = x.rstrip()
        v = x.split('\t')

        # Skip header
        if v[0] == "source":
            continue

        for term in v:
            # Pick cluster colour
            cluster_colour = default_colour
            if c < len(colours):
                cluster_colour = colours[c]
            # Is this the cluster label? Give it a bigger label size
            node_label_size = default_node_label_size
            if term == v[0]:
                node_label_size = cluster_label_size

            ann_out.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(term, c, v[0], ','.join([x for x in term_types[term]]), cluster_colour, node_label_size))
            if term not in term_to_cluster:
                term_to_cluster[term] = list()
            term_to_cluster[term] = [c, v[0]]
            #print('{} {} {} {}'.format(term, c, v[0], term_types[term]))

        c += 1

# Add in terms which had no cluster designation (orphans)
for t in gene_names:
    tname = term_names[t]
    print(tname)
    # If this term does not have a cluster?
    if tname not in term_to_cluster:
        # Add it to the cluster dict
        term_to_cluster[tname] = list()
        term_to_cluster[tname] = [c, tname]
        #Pick a colour
        cluster_colour = default_colour
        if c < len(colours):
            cluster_colour = colours[c]
        # Add orphan cluster information to the cluster annotation file
        ann_out.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(tname, c, tname, ','.join([x for x in term_types[tname]]), cluster_colour, cluster_label_size))
        # increment cluster counter
        c += 1

ann_out.close()


# Write out gProfiler results, with cluster included
gprof_outfile = outstem+'.gprofiler.tsv'
gprof_out = open(gprof_outfile, 'w')

with open(data) as d:
    for x in d.readlines():
        # query	significant	p_value	term_size	query_size	intersection_size	precision	recall	term_id	source	term_name	effective_domain_size	source_order	evidence_codes	intersection
        x = x.rstrip()
        v = x.split('\t')
        # print header
        if v[0] == 'query':
            gprof_out.write('\t{}\tclust_number\tclust_name\t{}\n'.format('\t'.join(v[0:11]), '\t'.join(v[11:])))
            continue

        clust_name = ''
        clust_number = ''
        print(v[11])
        if v[11] in term_to_cluster:
            clust_name = term_to_cluster[v[11]][1]
            clust_number = term_to_cluster[v[11]][0]

        gprof_out.write('{}\t{}\t{}\t{}\n'.format('\t'.join(v[0:12]), clust_number, clust_name, '\t'.join(v[12:])))

gprof_out.close()

# Outputs: network file, cluster annotations
print("Output files:\n  Network: {}\n  Clusters: {}\n  Annotation: {}\n gProfiler extended output: {}\n".format(network_outfile, clusters_outfile_name, ann_outfile, gprof_outfile))


