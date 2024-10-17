rule run_gprofiler:
    input:
        "{name}.list",
    params:
        species = "hsapiens",
    output:
        "gprofiler/{name}.gprofiler.out"
    shell:
        "Rscript run_gprofiler.R {input} {output} {params.species}"


rule run_funjacc:
    input:
        "gprofiler/{name}.gprofiler.out"
    params:
        function_types = "GO:BP,GO:MF,GO:CC,CORUM,KEGG,REAC,WP,TF",
        p_cut = 0.01,
        jacc_cut = 0.5,
        inflation = 1.4,
        outdir = "funjacc_res"
    output:
        "funjacc_res/{name}.gprofiler.tsv",
        "funjacc_res/{name}.ntwrk.txt",
        "funjacc_res/{name}.ann.txt"
    shell:
        "python3 funjacc.py -g {input} -d {params.function_types} -p {params.p_cut} " \
        "-j {params.jacc_cut} -I {params.inflation} -o {params.outdir}"