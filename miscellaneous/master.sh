#!/bin/bash
set -e
cd `dirname $0`

trial_num="260th"
primary_id="B047-683-2023-BL-BM1"
control_id="B042-683-2023-BL-SW1"
panel_id="B042-682-2022-HCL-SW1"


input_snv_self="/Volumes/My Book Duo/${trial_num}/mutation/${primary_id}_vs_${control_id}/yokomon/${primary_id}_vs_${control_id}.genomon_mutation.result.filt_nofilt.all.combined.yokomon_out_v6.1.tsv"
input_snv_other="/Volumes/My Book Duo/${trial_num}/mutation/${primary_id}_vs_${panel_id}/yokomon/${primary_id}_vs_${panel_id}.genomon_mutation.result.filt_nofilt.all.combined.yokomon_out_v6.1.tsv"
input_sv_self="/Volumes/My Book Duo/${trial_num}/sv/${primary_id}_vs_${control_id}/${primary_id}_vs_${control_id}.genomonSV.result.txt"
input_sv_other="/Volumes/My Book Duo/${trial_num}/sv/${primary_id}_vs_${panel_id}/${primary_id}_vs_${panel_id}.genomonSV.result.txt"
input_cnv="/Users/fukushimahideto/Desktop/${primary_id}_vs_${control_id}/${primary_id}_vs_${control_id}.out.fit.csv"
input_bam_tumor="/Volumes/My Book Duo/${trial_num}/bam/${primary_id}_vs_${control_id}/${primary_id}_vs_${control_id}.markdup.bam"
input_bam_normal="/Volumes/My Book Duo/${trial_num}/bam/${control_id}/${control_id}.markdup.bam"

output_dir_snv=/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/output/snv
output_dir_sv=/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/output/sv
output_dir_cnv=/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/output/cnv
output_dir_igv=/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/output/
output_snv_file1=${output_dir_snv}/snv_output1.tsv
output_snv_file2=${output_dir_snv}/snv_output1_anno.csv
output_snv_file3=${output_dir_snv}/snv_output2.csv
output_snv_filemyc=${output_dir_snv}/snv_output_myc.csv
output_sv_file=${output_dir_sv}/sv_output.tsv
output_cnv_file=${output_dir_cnv}/cnv_output.tsv

refflat_file=./database/refFlat.txt
jsh_file=./new_annotation_list/for_cnv.tsv

flag_snv=0
flag_sv=0
flag_cnv=0
flag_igv_snv=0
flag_igv_sv=0
flag_igv_peek=1
flag_pptx=0
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

#SNV

if [ $flag_snv == 1 ]; then
	echo "snv"
	echo "input file1 = ${input_snv_self}"
	echo "input file2 = ${input_snv_other}"
	/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/for_snv.sh "${input_snv_self}" "${input_snv_other}" "${output_snv_file1}" 
	echo "output is in ${output_dir_snv}"
	echo "completed process1"
	echo "start process2"
	Rscript /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/for_snv.R "${output_snv_file1}"
	echo "completed process2"
	/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/for_snv_myc.sh "${input_snv_self}" "${input_snv_other}" "${output_snv_filemyc}" 
	echo "completed process_myc"
fi




##############################################################################
##############################################################################
##############################################################################
##############################################################################



##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

#SV

if [ $flag_sv == 1 ]; then
	echo "Hello"
	echo "------------------------------------------------"
	echo "start sv annotation"
	echo "input file1 = ${input_sv_self}"
	echo "input file2 = ${input_sv_other}"
	echo "------------------------------------------------"
	python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/for_sv.py -i1 "${input_sv_self}" -i2 "${input_sv_other}" -o "${output_sv_file}"
	echo "output is in ${output_dir_sv}"
	echo "completed sv filtering"
fi



##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

#CNV

if [ $flag_cnv == 1 ]; then
	echo "Hello"
	echo "------------------------------------------------"
	echo "start cnv annotation"
	echo "input file = ${input_cnv}"
	echo "------------------------------------------------"	
	python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/for_cnv.py -i ${input_cnv} -o ${output_cnv_file} -r ${refflat_file} -c ${jsh_file}
	echo "output is in ${output_cnv_file}"
	echo "completed cnv filtering and annotation"	
fi

##############################################################################
##############################################################################

#IGV_SNV

if [ $flag_igv_snv == 1 ]; then
	echo "snapshot IGV_snv"
	echo "------------------------------------------------"
	echo "input bam1 = ${input_bam_self}"
	echo "input bam2 = ${input_bam_other}"
	echo "------------------------------------------------"
	export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home
	target_file=${output_dir_snv}/snv_output1all_anno.csv
	tail -n +2 "${target_file}" | while IFS=',' read -r somatic MYC VF VF_Normal Fisher Chr Start _; do
		echo "somatic=${somatic}, myc=${MYC}, vf=${VF}, vf_normal=${VF_Normal}, fisher=${Fisher}, chr=${Chr}, start=${Start}"
	    python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/snapshot_snv.py "$Chr" "$Start" "${input_bam_tumor}" "${input_bam_normal}" "${output_dir_igv}"
	done 
fi


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

#IGV_SV

if [ $flag_igv_sv == 1 ]; then
	echo "snapshot IGV_sv"
	echo "------------------------------------------------"
	echo "input bam1 = ${input_bam_tumor}"
	echo "input bam2 = ${input_bam_normal}"
	echo "------------------------------------------------"
	export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home
	target_file=${output_dir_sv}/sv_output.tsv
	tail -n +2 "${target_file}" | while IFS=$'\t' read -r Chr_1 Pos_1 Dir_1 Chr_2 Pos_2 _; do
		echo "sv events are as follows"
		echo "Chr_1=${Chr_1}, Pos_1=${Pos_1}, Chr_2=${Chr_2}, Pos_2=${Pos_2}"
	    python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/snapshot_sv.py "$Chr_1" "$Pos_1" "${input_bam_tumor}" "${input_bam_normal}" "${output_dir_igv}"
		python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/snapshot_sv.py "$Chr_2" "$Pos_2" "${input_bam_tumor}" "${input_bam_normal}" "${output_dir_igv}"
	done 
fi


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

#IGV_PEEK

if [ $flag_igv_peek == 1 ]; then
	echo "peek IGV"
	echo "------------------------------------------------"
	export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home
	python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/igv.py 
fi


##############################################################################
##############################################################################

#create pptx
if [ $flag_pptx == 1 ]; then
	echo "snapshot IGV_snv"
	echo "------------------------------------------------"
	echo "input bam1 = ${input_bam_self}"
	echo "input bam2 = ${input_bam_other}"
	echo "------------------------------------------------"
	python /Users/fukushimahideto/Desktop/clinical_sequencing_workflow/module/create_pptx.py
fi