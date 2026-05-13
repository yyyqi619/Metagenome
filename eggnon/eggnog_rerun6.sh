#!/bin/bash
#$ -S /bin/bash
#$ -N egg6_rerun
#$ -cwd
#$ -V
#$ -l h_vmem=16G
#$ -o logs/
#$ -e logs/

cd /export2/home/yanqi/project/mangrove/Ana_67MAG

OUTROOT=/export2/home/yanqi/project/mangrove/Ana_67MAG/eggnog
export EGGNOG_DATA_DIR=/export2/home/yanqi/databases/eggnog

faa=$(sed -n "${SGE_TASK_ID}p" rerun_6_faa_list.txt)

prefix=$(basename "$faa" .faa)
outdir="$OUTROOT/$prefix"
tmpdir="/tmp/$USER/emapper_$prefix"

mkdir -p "$outdir" "$tmpdir" logs

echo "[INFO] SGE_TASK_ID=$SGE_TASK_ID"
echo "[INFO] Running $prefix from $faa"

emapper.py \
  -i "$faa" \
  --itype proteins \
  --cpu 8 \
  --data_dir "$EGGNOG_DATA_DIR" \
  --output "$prefix" \
  --output_dir "$outdir" \
  --temp_dir "$tmpdir" \
  --override

rm -rf "$tmpdir"
