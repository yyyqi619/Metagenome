import os
import glob
from Bio import SeqIO

def parse_domtblout_results(domtblout_file, faa_sequences):
    """解析 domtblout 文件以获取比对片段的起始和结束位置并提取片段序列"""
    print(f"正在解析文件: {domtblout_file}")
    fragments = {}
    with open(domtblout_file, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue  # 跳过注释行
            
            columns = line.split()
            if len(columns) < 22:
                print(f"行数据不足，跳过: {line.strip()}")
                continue  # 确保行中有足够的列
            
            seq_id = columns[0]
            try:
                start = int(columns[19])  # 比对片段起始位置
                end = int(columns[20])    # 比对片段结束位置
            except ValueError:
                print(f"无法转换起始/结束位置为整数，跳过: {columns}")
                continue  # 如果起始或结束位置无法转换为整数，跳过该行
            
            # 提取片段真实序列并保存
            if seq_id in faa_sequences:
                fragment_seq = str(faa_sequences[seq_id].seq[start-1:end])
                if seq_id not in fragments:
                    fragments[seq_id] = []
                fragments[seq_id].append(fragment_seq)
                print(f"成功添加片段：{seq_id}, 起始: {start}, 结束: {end}, 片段长度: {len(fragment_seq)}")
            else:
                print(f"警告: {seq_id} 不在提供的 .faa 文件中")
    
    if not fragments:
        print(f"文件 {domtblout_file} 中没有找到任何有效的片段")
    return fragments

def merge_fragments(fragments, output_fasta):
    """将片段拼接成新序列并保存到 Fasta 文件中"""
    print(f"开始拼接片段并写入文件: {output_fasta}")
    with open(output_fasta, "w") as output:
        for seq_id, sequences in fragments.items():
            merged_seq = ''.join(sequences)  # 拼接所有片段为一个完整序列
            output.write(f">{seq_id}\n{merged_seq}\n")
            print(f"成功写入拼接序列: {seq_id}, 总长度: {len(merged_seq)}")

# 设置输入和输出路径
input_faa_dir = "/Users/MycologyLab/yanqi/tree_1025/faa_files/" #氨基酸原始序列
output_dir = "/Users/MycologyLab/yanqi/tree_1025/hmm/" #序列end和start文件
output_fasta_dir = "/Users/MycologyLab/yanqi/tree_1025/merged_sequences1105/"#拼接文件输出文件

# 确保输出目录存在
os.makedirs(output_fasta_dir, exist_ok=True)

# 列出输入目录和比对结果目录中的文件，便于调试
print("输入目录中的文件:", os.listdir(input_faa_dir))
print("比对结果目录中的文件:", os.listdir(output_dir))

# 遍历每个比对结果文件
for domtblout_file in glob.glob(output_dir + "*_hmmsearch.txt"):
    base_name = os.path.basename(domtblout_file).replace("_hmmsearch.txt", "")
    faa_file = f"{input_faa_dir}/{base_name}.faa"
    output_fasta = f"{output_fasta_dir}/{base_name}_merged.fasta"
    
    print(f"正在处理文件: {domtblout_file}")
    
    # 检查 .faa 文件是否存在
    if not os.path.exists(faa_file):
        print(f"错误：输入 .faa 文件未找到: {faa_file}")
        continue
    
    # 读取 .faa 文件中的序列信息
    try:
        faa_sequences = {record.id: record for record in SeqIO.parse(faa_file, "fasta")}
        print(f"读取 {len(faa_sequences)} 个序列自 {faa_file}")
    except Exception as e:
        print(f"读取 .faa 文件时出错: {e}")
        continue
    
    # 解析比对结果并提取实际序列片段
    fragments = parse_domtblout_results(domtblout_file, faa_sequences)
    
    # 确保解析后的片段不为空再尝试拼接
    if fragments:
        merge_fragments(fragments, output_fasta)
        print(f"输出文件生成成功: {output_fasta}")
    else:
        print(f"警告：未生成输出文件，因为 {domtblout_file} 中没有有效片段")
