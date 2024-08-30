import csv
with open('/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/new_annotation_list/AGMC_V3_1.csv', 'rt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')

	with open('/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/new_annotation_list/AGMC_V3_1.tsv', 'wt',newline='') as tsv_file:
		tsv_writer = csv.writer(tsv_file, delimiter='\t')

		for row in csv_reader:
			tsv_writer.writerow(row)