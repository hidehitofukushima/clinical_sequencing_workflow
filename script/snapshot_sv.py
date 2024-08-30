import sys
import subprocess
import os

# sys.argv[0]には実行したスクリプト名が格納されています
script_name = sys.argv[0]

# sys.argv[1]には1つ目の引数が格納されています（この場合はchr）
chr_value = sys.argv[1]

# sys.argv[2]には2つ目の引数が格納されています（この場合はpos）
pos_value = sys.argv[2]

input_bam_tumor = sys.argv[3]
input_bam_normal = sys.argv[4]
output_dir_igv = sys.argv[5]


# 得られた引数を使って処理を行う例
print(
    f"{chr_value}, {pos_value}, {input_bam_tumor}, {input_bam_normal}, {output_dir_igv}"
)

script_dir = output_dir_igv + "/igv_sv"
output_dir = output_dir_igv + "/igv_sv"
script_file = output_dir_igv + "/igv_sv/" + \
    chr_value + "_" + pos_value + ".batch"

# scriptフォルダの作成
# snapshotフォルダの作成
try:
    os.makedirs(script_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
except FileExistsError as e:
    print("ディレクトリの作成に失敗しました:", e)


batch = """
    new
    snapshotDirectory {output_dir}
    genome hg19
    load "{input_bam_tumor}"
    load "{input_bam_normal}"
    maxPanelHeight 300
    viewaspairs
    preference SAM.SHOW_SOFT_CLIPPED true
    goto chr{chr}:{pos1}-{pos2}
    group reference_concordance
    sort base 
    collapse
    snapshot collapse_{chr}_{pos}.png
    squish 
    snapshot squish_{chr}_{pos}.png
    exit
    
"""

with open(script_file, "w") as script_handle:
    tmp = batch.format(
        chr=chr_value,
        pos=pos_value,
        pos1=int(pos_value) - 100,
        pos2=int(pos_value) + 100,
        output_dir=output_dir,
        input_bam_tumor=input_bam_tumor,
        input_bam_normal=input_bam_normal,
    )
    script_handle.write(tmp)


cmd = "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/IGV_2.18.2/igv.sh -b " + script_file
print(cmd)
sp = subprocess.Popen(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out_msg, err_msg = sp.communicate()

exit_code = sp.wait()

if exit_code != 0:
    print(f"Error: Process exited with non-zero status code {exit_code}")

if out_msg:
    print("Standard Output:")
    print(out_msg.decode())

if err_msg:
    print("Standard Error:")
    print(err_msg.decode())
