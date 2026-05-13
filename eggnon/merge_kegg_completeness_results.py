import os
import glob
import pandas as pd

indir = "kegg_completeness_results"
out_file_long = "all_MAGs_kegg_module_completeness_long.csv"
out_file_matrix = "all_MAGs_kegg_module_completeness_matrix.csv"

files = glob.glob(os.path.join(indir, "*_pathways.tsv"))

all_results = []

for file in files:
    mag_name = os.path.basename(file).replace("_pathways.tsv", "")

    df = pd.read_csv(file, sep="\t")
    df.insert(0, "MAG", mag_name)

    all_results.append(df)

merged = pd.concat(all_results, ignore_index=True)

merged.to_csv(out_file_long, index=False)

matrix = merged.pivot_table(
    index="module_accession",
    columns="MAG",
    values="completeness",
    fill_value=0
)

matrix.to_csv(out_file_matrix)

print(f"Long table saved to: {out_file_long}")
print(f"Matrix table saved to: {out_file_matrix}")
