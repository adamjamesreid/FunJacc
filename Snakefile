# AUTHOR: Adam James Reid
# Copyright (C) 2024 University of Cambridge
# This program is distributed under the terms of the GNU General Public License

configfile: "config.yaml"

rule run_gprofiler:
    input:
        "input/{name}.list",
    params:
        species = config["organism"]
    output:
        "gprofiler/{name}.gprofiler.out"
    shell:
        "Rscript run_gprofiler.R {input} {output} {params.species}"


rule run_funjacc:
    input:
        "gprofiler/{name}.gprofiler.out"
    params:
        function_types = config['function_types'],
        p_cut = config['p_cut'],
        jacc_cut = config['jacc_cut'],
        inflation = config['inflation'],
        outdir = "funjacc_res"
    output:
        "funjacc_res/{name}.gprofiler.tsv",
        "funjacc_res/{name}.ntwrk.txt",
        "funjacc_res/{name}.ann.txt"
    shell:
        "python3 funjacc.py -g {input} -d {params.function_types} -p {params.p_cut} " \
        "-j {params.jacc_cut} -I {params.inflation} -o {params.outdir}"
