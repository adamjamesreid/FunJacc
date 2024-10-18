# AUTHOR: Adam James Reid
# Copyright (C) 2024 University of Cambridge
# This program is distributed under the terms of the GNU General Public License

# USAGE
#Rscript run_gprofiler.R <gene_list> <output_file> <organism>

library(gprofiler2)

# test if there is at least one argument: if not, return an error
args = commandArgs(trailingOnly=TRUE)

if (length(args) < 3) {
  stop("USAGE: Rscript run_gprofiler.R <gene_list> <output_file> <organism e.g. hsapiens>", call.=FALSE)
} 

# Read in command line arguments
gene_list <- read.csv(args[1], header=FALSE)
output_file <- args[2]
organism <- args[3]

# Run gProfiler (evcodes =TRUE gives us the genes associated with each term)
gprof_res <- gost(query = gene_list$V1,
                              organism = organism, evcodes = TRUE)

# Filter out difficult "parents" column (it is really a list)
gprof_res <- gprof_res$result[, -which(colnames(gprof_res$result) %in% c("parents"))]

# Write results to a file
write.table(gprof_res, file=output_file, quote=FALSE, sep="\t")
