import pandas as pd
import os
import glob

folder_path = "/export2/home/yanqi/project/mangrove/Ana_67MAG/eggnog/"

columns_to_count = [
    'GOs', 'EC', 'KEGG_ko', 'KEGG_Pathway', 'KEGG_Module',
    'KEGG_Reaction', 'KEGG_rclass', 'BRITE', 'KEGG_TC',
    'CAZy', 'BiGG_Reaction', 'PFAMs'
]

result_file_name = "results_0513.xlsx"

annotation_files = glob.glob(
    os.path.join(folder_path, "**", "*.emapper.annotations"),
    recursive=True
)

print(f"Found {len(annotation_files)} annotation files")

if len(annotation_files) == 0:
    raise ValueError("No *.emapper.annotations files found.")

result_dict = {}

for file_path in annotation_files:
    sample_name = os.path.basename(os.path.dirname(file_path))
    print(f"\nReading: {sample_name}")

    # 找到真正的表头行，一般是以 #query 开头
    header = None
    skiprows = 0

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if line.startswith("#query"):
                header = line.strip().lstrip("#").split("\t")
                skiprows = i + 1
                break

    if header is None:
        print(f"Warning: no header line found in {sample_name}")
        continue

    df = pd.read_csv(
        file_path,
        sep="\t",
        names=header,
        skiprows=skiprows,
        comment="#",
        low_memory=False
    )

    print("Detected columns:")
    print(df.columns.tolist())

    matched_columns = [c for c in columns_to_count if c in df.columns]

    if len(matched_columns) == 0:
        print(f"Warning: no target columns found in {sample_name}")
        continue

    for column_name in matched_columns:
        elements = (
            df[column_name]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
        )

        elements = elements[(elements != "") & (elements != "-")]

        counts = elements.value_counts()
        df_count = pd.DataFrame({sample_name: counts})

        if column_name in result_dict:
            result_dict[column_name] = pd.concat(
                [result_dict[column_name], df_count],
                axis=1
            )
        else:
            result_dict[column_name] = df_count

if len(result_dict) == 0:
    raise ValueError(
        "No results generated. Please check whether eggNOG column names match target columns."
    )

with pd.ExcelWriter(result_file_name, engine="openpyxl") as writer:
    for sheet_name, df_out in result_dict.items():
        df_out.to_excel(writer, sheet_name=sheet_name[:31])

print(f"\nDone. Results saved to: {result_file_name}")
