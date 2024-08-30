import os
import subprocess
import configparser
import time
import csv
import shutil
import script.snapshot_snv as snapshot_snv
import script.for_snv_multifilter as snv_multifilter

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")


# --------------------------------------------------
# config,iniから値取得
# --------------------------------------------------
# config.iniの値取得その1

trial_num = config_ini["MAIN"]["trial_num"]
primary_id = config_ini["MAIN"]["primary_id"]
control_id = config_ini["MAIN"]["control_id"]
panel_id = config_ini["MAIN"]["panel_id"]

flag_initialize = int(config_ini["FLAG"]["initialize"])
flag_snv = int(config_ini["FLAG"]["snv"])
flag_snv_multifilter = int(config_ini["FLAG"]["snv_multifilter"])
flag_sv = int(config_ini["FLAG"]["sv"])
flag_cnv = int(config_ini["FLAG"]["cnv"])
flag_igv_snv = int(config_ini["FLAG"]["igv_snv"])
flag_igv_sv = int(config_ini["FLAG"]["igv_sv"])
flag_igv_peek = int(config_ini["FLAG"]["igv_peek"])
flag_pptx = int(config_ini["FLAG"]["pptx"])


data_path_trunk = config_ini["PATH"]["trunk"]
output_trunk = config_ini["PATH"]["output"]
database_refflat = config_ini["PATH"]["refflat"]
database_cnv = config_ini["PATH"]["cnv"]
database_sv = config_ini["PATH"]["sv"]


input_snv_self = f"{data_path_trunk}/{trial_num}/mutation/{primary_id}_vs_{control_id}/yokomon/{primary_id}_vs_{control_id}.genomon_mutation.result.filt_nofilt.all.combined.yokomon_out_v6.1.tsv"
input_snv_other = f"{data_path_trunk}/{trial_num}/mutation/{primary_id}_vs_{panel_id}/yokomon/{primary_id}_vs_{panel_id}.genomon_mutation.result.filt_nofilt.all.combined.yokomon_out_v6.1.tsv"
input_sv_self = f"{data_path_trunk}/{trial_num}/sv/{primary_id}_vs_{control_id}/{primary_id}_vs_{control_id}.genomonSV.result.txt"
# input_sv_self = f"/Users/fukushimahideto/Desktop/{primary_id}_vs_{control_id}/{primary_id}_vs_{panel_id}.genomonSV.result.filt.txt"
# input_sv_other = f"/Users/fukushimahideto/Desktop/{primary_id}_vs_{control_id}/{primary_id}_vs_{panel_id}.genomonSV.result.filt.txt"
input_sv_other = f"{data_path_trunk}/{trial_num}/sv/{primary_id}_vs_{panel_id}/{primary_id}_vs_{panel_id}.genomonSV.result.txt"
# input_cnv = f"/Users/fukushimahideto/Desktop/{primary_id}_vs_{control_id}/{primary_id}_vs_{control_id}.out.fit.csv"
input_cnv = f"{data_path_trunk}/{trial_num}/facets/{primary_id}_vs_{control_id}/{primary_id}_vs_{control_id}.out.fit.tsv"
input_bam_tumor = f"{data_path_trunk}/{trial_num}/bam/{primary_id}_vs_{control_id}/{primary_id}_vs_{control_id}.markdup.bam"
input_bam_normal = (
    f"{data_path_trunk}/{trial_num}/bam/{control_id}/{control_id}.markdup.bam"
)

output_dir_snv = f"{output_trunk}/snv"
output_dir_snv_multifilter = f"{output_trunk}/snv_multifilter"
output_dir_sv = f"{output_trunk}/sv"
output_dir_cnv = f"{output_trunk}/cnv"
output_dir_igv_snv = f"{output_trunk}/igv_snv"
output_dir_igv_sv = f"{output_trunk}/igv_sv"
output_snv_file1 = f"{output_dir_snv}/snv_output1.tsv"
output_snv_file2 = f"{output_dir_snv}/snv_output1_anno.csv"
output_snv_file3 = f"{output_dir_snv}/snv_output2.csv"
output_snv_filemyc = f"{output_dir_snv}/snv_output_myc.csv"
output_sv_file = f"{output_dir_sv}/sv_output.tsv"
output_cnv_file = f"{output_dir_cnv}/cnv_output.tsv"

refflat_file = database_refflat
jsh_file = database_cnv

# initialize
if flag_initialize == 1:
    print("Initializing")
    if os.path.exists(output_trunk):
        shutil.rmtree(output_trunk)
    os.mkdir(output_trunk)
    os.mkdir(output_dir_snv)
    os.mkdir(output_dir_sv)
    os.mkdir(output_dir_cnv)
    os.mkdir(output_dir_snv_multifilter)
    os.mkdir(output_dir_igv_snv)


# SNV
if flag_snv == 1:
    print("snv")
    time.sleep(2)
    # Run the shell script
    subprocess.run(
        [
            "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/for_snv.sh",
            input_snv_self,
            input_snv_other,
            output_snv_file1,
        ]
    )
    subprocess.run(
        [
            "Rscript",
            "--vanilla",
            "-e",
            ".libPaths('/Library/Frameworks/R.framework/Versions/4.4-arm64/Resources/library/clinical_sequencing_workflow'); source('/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/for_snv.R')",
            output_snv_file1,
        ]
    )
    # subprocess.run(
    #     [
    #         "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/for_snv_myc.sh",
    #         input_snv_self,
    #         input_snv_other,
    #         output_snv_filemyc,
    #     ]
    # )
    print("completed process_myc")
    time.sleep(2)


# SV
if flag_sv == 1:
    print("sv")

    # Run the Python script
    subprocess.run(
        [
            "python3",
            "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/for_sv.py",
            "-i1",
            input_sv_self,
            "-i2",
            input_sv_other,
            "-o",
            output_sv_file,
            "-s",
            database_sv,

        ]
    )

    print("completed sv filtering")


# CNV
if flag_cnv == 1:
    print("cnv")

    # Run the Python script
    subprocess.run(
        [
            "python3",
            "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/for_cnv.py",
            "-i",
            input_cnv,
            "-o",
            output_cnv_file,
            "-r",
            refflat_file,
            "-c",
            jsh_file,
        ]
    )

    print("completed cnv filtering and annotation")


# SNV_MULTIFILTER
if flag_snv_multifilter == 1:
    print("snv_multifilter")
    target_file_cosmic = f"{output_dir_snv}/snv_output1cosmic_anno.tsv"
    target_file_germline = f"{output_dir_snv}/snv_output1germline_anno.tsv"
    target_file_trunc = f"{output_dir_snv}/snv_output1trunc_anno.tsv"
    output_file_snv_multifilter_cosmic = f"{output_dir_snv_multifilter}/snv_mf_cosmic.tsv"
    output_file_snv_multifilter_germline = f"{output_dir_snv_multifilter}/snv_mf_germline.tsv"
    output_file_snv_multifilter_trunc = f"{output_dir_snv_multifilter}/snv_mf_trunc.tsv"

    snv_multifilter.multifilter(target_file_cosmic, input_bam_tumor,
                                input_bam_normal, output_file_snv_multifilter_cosmic)
    snv_multifilter.multifilter(target_file_germline, input_bam_tumor,
                                input_bam_normal, output_file_snv_multifilter_germline)
    snv_multifilter.multifilter(target_file_trunc, input_bam_tumor,
                                input_bam_normal, output_file_snv_multifilter_trunc)


# IGV_SNV
if flag_igv_snv == 1:
    print("snapshot IGV_snv")

    # Set the JAVA_HOME environment variable
    os.environ[
        "JAVA_HOME"
    ] = "/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home"
    target_file_cosmic = f"{output_dir_snv_multifilter}/snv_mf_cosmic.tsv"
    target_file_germline = f"{output_dir_snv_multifilter}/snv_mf_germline.tsv"
    target_file_trunc = f"{output_dir_snv_multifilter}/snv_mf_trunc.tsv"
    output_dir_igv_snv_cosmic = f"{output_dir_igv_snv}/cosmic"
    output_dir_igv_snv_germline = f"{output_dir_igv_snv}/germline"
    output_dir_igv_snv_trunc = f"{output_dir_igv_snv}/trunc"
    os.mkdir(output_dir_igv_snv_cosmic)
    os.mkdir(output_dir_igv_snv_germline)
    os.mkdir(output_dir_igv_snv_trunc)

    snapshot_snv.snap(target_file_cosmic, input_bam_tumor,
                      input_bam_normal, output_dir_igv_snv_cosmic)
    snapshot_snv.snap(target_file_germline, input_bam_tumor,
                      input_bam_normal, output_dir_igv_snv_germline)
    snapshot_snv.snap(target_file_trunc, input_bam_tumor,
                      input_bam_normal, output_dir_igv_snv_trunc)


# IGV_SV
if flag_igv_sv == 1:
    print("snapshot IGV_sv")
    print("------------------------------------------------")
    print(f"input bam1 = {input_bam_tumor}")
    print(f"input bam2 = {input_bam_normal}")
    print("------------------------------------------------")

    # Set the JAVA_HOME environment variable
    os.environ[
        "JAVA_HOME"
    ] = "/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home"

    target_file = f"{output_dir_sv}/sv_output.tsv"

    # Open the TSV file and skip the header
    with open(target_file, "r") as f:
        tsv_reader = csv.reader(f, delimiter="\t")
        next(tsv_reader)

        # Loop through each row in the TSV file
        for row in tsv_reader:
            Chr_1, Pos_1, Dir_1, Chr_2, Pos_2, *_ = row
            print("sv events are as follows")
            print(
                f"Chr_1={Chr_1}, Pos_1={Pos_1}, Chr_2={Chr_2}, Pos_2={Pos_2}")

            # Run the Python script
            subprocess.run(
                [
                    "python3",
                    "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/snapshot_sv.py",
                    Chr_1,
                    Pos_1,
                    input_bam_tumor,
                    input_bam_normal,
                    output_dir_igv_sv
                ]
            )
            subprocess.run(
                [
                    "python3",
                    "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/snapshot_sv.py",
                    Chr_2,
                    Pos_2,
                    input_bam_tumor,
                    input_bam_normal,
                    output_dir_igv_sv,
                ]
            )


# IGV_PEEK
if flag_igv_peek == 1:
    print("peek IGV")
    print("------------------------------------------------")

    # Set the JAVA_HOME environment variable
    os.environ[
        "JAVA_HOME"
    ] = "/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home"

    # Run the Python script
    subprocess.run(
        [
            "python",
            "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/igv.py",
        ]
    )

# create pptx
if flag_pptx == 1:
    print("create pptx template")

    # Run the Python script
    subprocess.run(
        [
            "python",
            "/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/script/create_pptx.py",
        ]
    )
