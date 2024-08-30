#!/bin/bash

input_file_somatic=$1
input_file_all=$2
output_file=$3
echo input_file_somatic: $input_file_somatic
echo input_file_all: $input_file_all
echo output_file: $output_file
awk -F'\t' -v 'OFS=\t' '((NR == 1) || ($21 == "exonic") || ($21 == "splicing")) && $24 != "synonymous SNV" {print "somatic",$1,$2,$3,$4,$13,$14,$15,$16,$17,$21,$22,$24,$25,$41,$135,$138,$145,$152,$230,$231,$232}' "$input_file_somatic" > "$output_file"
awk -F'\t' -v 'OFS=\t' '(($21 == "exonic") || ($21 == "splicing")) && $24 != "synonymous SNV" {print "all",$1,$2,$3,$4,$13,$14,$15,$16,$17,$21,$22,$24,$25,$41,$135,$138,$145,$152,$230,$231,$232}' "$input_file_all" >> "$output_file"


