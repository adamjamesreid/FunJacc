library(gprofiler2)


# USAGE
#Rscript run_gprofiler.R <gene_list> <output_file> <organism>

# test if there is at least one argument: if not, return an error
args = commandArgs(trailingOnly=TRUE)

if (length(args) < 3) {
  stop("USAGE: Rscript run_gprofiler.R <gene_list> <output_file> <organism e.g. hsapiens>", call.=FALSE)
} 

#print(args)

gene_list <- read.csv(args[1], header=FALSE)
output_file <- args[2]
organism <- args[3]

# Run gProfiler (evcodes =TRUE gives us the genes associated with each term)
gprof_res <- gost(query = gene_list$V1,
                              organism = organism, evcodes = TRUE)

# Plot results
#gostplot(KD_in_High_go_terms, capped = TRUE, interactive = TRUE)

# Filter out difficult "parents" column (it is really a list)
gprof_res <- gprof_res$result[, -which(colnames(gprof_res$result) %in% c("parents"))]

# Write results to a file
write.table(gprof_res, file=output_file, quote=FALSE, sep="\t")
