rule run_gprofiler:
    input:
        "{name}.list",
    params:
        species = "hsapiens",
        #outfile_name = "gprofiler/test.out"
    output:
        "{name}.gprofiler.out"
    shell:
        "Rscript run_gprofiler.R {input} {output} {params.species}"

rule run_funjacc:
    input:
        "{name}.gprofiler.out"
    params:
        function_types = "GO:BP,GO:MF,GO:CC,CORUM,KEGG,REAC,WP,TF",
        p_cut = 0.01,
        jacc_cut = 0.5,
        inflation = 1.4
    output:
        "{name}.gprofiler.tsv",
        "{name}.ntwrk.txt",
        "{name}.ann.txt"
    shell:
        "python3 funjacc.py -g {input} -d {params.function_types} -p {params.p_cut} " \
        "-j {params.jacc_cut} -I {params.inflation}"