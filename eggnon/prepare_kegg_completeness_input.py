import os
import pandas as pd

input_file = "results_0513_ko.csv"
outdir = "kegg_completeness_input0513"

os.makedirs(outdir, exist_ok=True)

df = pd.read_csv(input_file)

# 第一列其实是 MAG/bin 名
mag_col = df.columns[0]

for _, row in df.iterrows():
    mag_name = str(row[mag_col])

    kos = []

    for ko in df.columns[1:]:
        value = row[ko]

        if pd.notna(value) and value > 0:
            kos.append(ko)

    kos = sorted(set(kos))

    out_file = os.path.join(outdir, f"{mag_name}.kos.txt")

    # give_completeness 的 --input-list 默认可以用逗号分隔
    with open(out_file, "w") as f:
        f.write(",".join(kos) + "\n")

print(f"Done. KO list files were written to: {outdir}")
