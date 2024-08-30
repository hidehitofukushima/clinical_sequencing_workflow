import sys
import subprocess
import os


# snapshot_snv.snap(target_file_trunc, input_bam_tumor,
#                      input_bam_normal, output_dir_igv_snv_trunc)
def snap(target_file, input_bam_tumor, input_bam_normal, output_dir_igv_snv):

    # Set the JAVA_HOME environment variable
    # export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home"
    os.environ[
        "JAVA_HOME"
    ] = "/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home"

    # parse target_file and create simple list
    with open(target_file, "rt") as f:
        next(f)
        mutation_list = []
        for line in f:
            line_list = line.rstrip().split('\t')
            # merged_flag	somatic	MYC	VF	VF_Normal	Fisher	Chr	Start	End	Ref	Alt	Func.refGene	Gene.refGene
            merged_flag, somatic, MYC, VF, VF_Normal, Fisher, Chr, Start, End, Ref, Alt, Func_refGene, Gene_refGene = [
                line_list[i] for i in range(0, 13)]
            # gene,start,posをリストに追加
            print(f'merged_flag= {merged_flag}')
            print(f'somatic= {somatic}')
            print(f'MYC= {MYC}')
            print(f'VF= {VF}')
            print(f'VF_Normal= {VF_Normal}')
            print(f'Fisher= {Fisher}')
            print(f'Chr= {Chr}')
            print(f'Start= {Start}')
            print(f'End= {End}')
            print(f'Ref= {Ref}')
            print(f'Alt= {Alt}')
            print(f'Func_refGene= {Func_refGene}')
            print(f'Gene_refGene= {Gene_refGene}')

            mutation_list.append([Gene_refGene, Start, Chr])
    # mutation_listの中にあるgene全てに対してigvでキャプチャをするように　batchを作成する
    # テンプレートのbatchを、header, body,footerに分けて作成する
    # header
    batch_header = """
    new
    snapshotDirectory {output_dir_igv}
    load "{input_bam_tumor}"
    load "{input_bam_normal}"
    genome hg19
    maxPanelHeight 1000
    viewaspairs
    preference SAM.SHOW_SOFT_CLIPPED true
    """
    # body
    batch_body = """
    goto chr{chr}:{pos}
    group base_at_pos chr{chr}:{pos}
    sort base 
    collapse
    snapshot collapse_{gene_value}_{chr}_{pos}.png
    squish 
    snapshot squish_{gene_value}_{chr}_{pos}.png
    """
    # footer
    batch_footer = """
    exit
    """
    # script_bufferを作成
    script_buffer = batch_header.format(
        output_dir_igv=output_dir_igv_snv,
        input_bam_tumor=input_bam_tumor,
        input_bam_normal=input_bam_normal,
    )

    # mutation_listの中にあるgene全てに対してigvでキャプチャをするように　batchを作成する
    for mutation in mutation_list:
        gene_value = mutation[0]
        pos_value = mutation[1]
        chr_value = mutation[2]

        script_buffer += batch_body.format(
            chr=chr_value,
            pos=pos_value,
            gene_value=gene_value,
        )
    # footerを追加
    script_buffer += batch_footer
    script_file = output_dir_igv_snv + '/' +\
        gene_value + "_" + chr_value + "_" + pos_value + ".batch"

    with open(script_file, "w") as script_handle:
        script_handle.write(script_buffer)
    cmd = "/Users/fukushimahideto/tools/IGV_2.17.2/igv.sh -b " + script_file
    print(cmd)
    sp = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out_msg, err_msg = sp.communicate()

    exit_code = sp.wait()

    if exit_code != 0:
        print(f"Error: Process exited with non-zero status code {exit_code}")
        print(f"Error: {err_msg.decode('utf-8')}")
