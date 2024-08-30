import subprocess
import os
import pysam

# multifilter 関数を実装する
# 入力例は、こんなかんじ　
# multifilter(target_file_cosmic, input_bam_tumor,
#                                input_bam_normal, output_file_snv_multifilter_cosmic)


def multifilter(target_file, input_bam_tumor, input_bam_normal, output_file):

    # まずは、target_fileの中身を読み込む
    with open(target_file, 'rt') as target_file_handle, open(output_file, 'wt') as output_file_handle:
        header_line = target_file_handle.readline()
        header_list = header_line.rstrip().split('\t')
        header_hash = {value: index for index, value in enumerate(header_list)}
        header_buffer = 'merged_flag' + '\t' + '\t'.join(header_list) + '\n'
        output_file_handle.write(header_buffer)

        # gene_list_all, gene_list_somaticを作成する
        gene_dict_all = {}
        gene_dict_somatic = {}

        # 1行ずつ読み込んでいく
        for line in target_file_handle:
            line_list = line.rstrip().split('\t')
            line_list_to_remove = ['somatic', 'MYC', 'VF', 'VF_Normal',
                                   'Fisher', 'TUMOR', 'NORMAL']

            remove_index = [header_hash[item] for item in line_list_to_remove]
            # line_list からremove_indexに該当する要素を削除する
            line_list_new = [item for index, item in enumerate(
                line_list) if index not in remove_index]
            somatic_all_flag = line_list[0]
            chr = line_list[header_hash['Chr']]
            pos = line_list[header_hash['Start']]
            merged_index = chr + ':' + pos

            # 1列目の値で、gene_list_all, gene_list_somaticに振り分ける
            if somatic_all_flag == 'somatic':
                gene_dict_somatic[merged_index] = line_list

            elif somatic_all_flag == 'all':
                gene_dict_all[merged_index] = line_list
            else:
                print(f'somatic_all_flag= {somatic_all_flag}')
                print(line_list)
                print('Error')

        # gene_list_allとgene_list_somaticを比較して、共通項には、先頭に'both'を追加
        # gene_list_allのみにあるものは、先頭に'leaked'を追加
        # gene_list_somaticのみにあるものは、先頭に'why only in somatic??'を追加
        # これらをすべて一つのリストに戻す
        gene_list = []
        for merged_index in gene_dict_all:
            if merged_index in gene_dict_somatic:
                list_somatic = gene_dict_somatic[merged_index]
                tumor = list_somatic[header_hash['TUMOR']]
                normal = list_somatic[header_hash['NORMAL']]
                supporting_tumor = tumor.split(':')[3].split(',')[1]
                supporting_normal = normal.split(':')[3].split(',')[1]
                depth_tumor = tumor.split(':')[2]
                depth_normal = normal.split(':')[2]
                vaf_tumor = tumor.split(':')[4]
                vaf_normal = normal.split(':')[4]
                merged_flag = f'both, tumor:{supporting_tumor}/{depth_tumor}({vaf_tumor}), normal:{supporting_normal}/{depth_normal}({vaf_normal})'

                # gene_list_somatic.remove(gene)これをdictで行う
                gene_dict_somatic.pop(merged_index)
                list_somatic = [merged_flag] + list_somatic
                write_buffer = '\t'.join(list_somatic) + '\n'
                output_file_handle.write(write_buffer)

            elif merged_index not in gene_dict_somatic:
                list_all = gene_dict_all[merged_index]

                chr = list_all[header_hash['Chr']]
                pos = list_all[header_hash['Start']]
                ref = list_all[header_hash['Ref']]
                alt = list_all[header_hash['Alt']]

                # input_bam_normalから、merged_indexの位置のリード数を塩基ごとに取得する
                bam_file = pysam.AlignmentFile(input_bam_normal, 'rb')

                reads = bam_file.fetch(chr, int(pos)-1, int(pos))

                base_counts = {'A': 0, 'T': 0, 'G': 0, 'C': 0, 'N': 0}
                for read in reads:
                    print('read')
                    print(read)
                    print(f'read.reference_start={read.reference_start}')
                    print(f'read.reference_end={read.reference_end}')
                    if read.reference_start is None or read.reference_end is None:
                        continue
                    if read.reference_start <= int(pos)-1 <= read.reference_end:
                        sequence_index = int(pos) - 1 - read.reference_start
                        if sequence_index < len(read.query_sequence):
                            base_counts[read.query_sequence[sequence_index]] += 1
                depth_normal = sum(base_counts.values())
                if alt in base_counts:
                    supporting_normal = base_counts[alt]
                    vaf_normal = supporting_normal / (depth_normal+0.01)

                else:
                    supporting_normal = ''
                    vaf_normal = ''

                bam_file.close()

                tumor = list_all[header_hash['TUMOR']]
                supporting_tumor = tumor.split(':')[3].split(',')[1]
                depth_tumor = tumor.split(':')[2]
                vaf_tumor = tumor.split(':')[4]
                merged_flag = f'leaked, tumor:{supporting_tumor}/{depth_tumor}({vaf_tumor}), normal:{supporting_normal}/{depth_normal}({vaf_normal})'

                list_all = [merged_flag] + list_all
                write_buffer = '\t'.join(list_all) + '\n'
                output_file_handle.write(write_buffer)

        # gene_dict_somaticの中身が残っていたら、それらについても、先頭に'why only in somatic??'を追加して、出力する
        for merged_index in gene_dict_somatic:
            list_somatic = gene_dict_somatic[merged_index]
            tumor = list_somatic[header_hash['TUMOR']]
            normal = list_somatic[header_hash['NORMAL']]
            supporting_tumor = tumor.split(':')[3].split(',')[1]
            supporting_normal = normal.split(':')[3].split(',')[1]
            depth_tumor = tumor.split(':')[2]
            depth_normal = normal.split(':')[2]
            vaf_tumor = tumor.split(':')[4]
            vaf_normal = normal.split(':')[4]
            merged_flag = f'why only in somatic??, tumor:{supporting_tumor}/{depth_tumor}({vaf_tumor}), normal:{supporting_normal}/{depth_normal}({vaf_normal})'
            list_somatic = [merged_flag] + list_somatic
            write_buffer = '\t'.join(list_somatic) + '\n'
            output_file_handle.write(write_buffer)


if __name__ == '__main__':
    target_file_cosmic = '/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/output/snv/snv_output1cosmic_anno.tsv'
    input_bam_tumor = '/Users/fukushimahideto/Desktop/ID697/bam/B035-697-2023-AML-PB1_vs_B035-697-2023-AML-SW1/B035-697-2023-AML-PB1_vs_B035-697-2023-AML-SW1.markdup.bam'
    input_bam_normal = '/Users/fukushimahideto/Desktop/ID697/bam/B035-697-2023-AML-SW1/B035-697-2023-AML-SW1.markdup.bam'
    output_file_snv_multifilter_cosmic = '/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/output/snv/snv_output2multifilter_cosmic.tsv'
    # main()
    multifilter(target_file_cosmic, input_bam_tumor,
                input_bam_normal, output_file_snv_multifilter_cosmic)
    print('Done')
