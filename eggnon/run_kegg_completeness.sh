#!/bin/bash

indir="kegg_completeness_input0513"
outdir="kegg_completeness_results"

mkdir -p ${outdir}

for file in ${indir}/*.kos.txt
do
    base=$(basename ${file} .kos.txt)

    echo "Processing ${base}"

    give_completeness \
        --input-list ${file} \
        --list-separator ',' \
        --outdir ${outdir} \
        --outprefix ${base}
done

echo "All done."
