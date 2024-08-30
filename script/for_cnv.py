import os
import sys
import argparse
import csv
from bisect import bisect_left
from bisect import bisect_right
import time
#
# Main
#


def convert_to_int(data):
    try:
        return int(data)
    except ValueError:
        return None


data = "NA"
converted_data = convert_to_int(data)


def create_index(refFlat_file):
    """
    Create an index of the chromosome positions of each gene in a refFlat.txt file.

    Parameters:
        refFlat_file (str): path to the refFlat.txt file

    Returns:
        index (dict): a dictionary mapping chromosome names to a list of tuples
                      representing the start and end positions of each gene
    """
    index = {}
    with open(refFlat_file, 'r') as f:
        for line in f:
            fields = line.strip().split('\t')
            chrom = fields[2]
            start = int(fields[4])
            end = int(fields[5])
            if chrom not in index:
                index[chrom] = []
            index[chrom].append((start, end, fields[0]))
    for chrom in index:
        index[chrom].sort()
    return index


def search_gene(refFlat_file, chrom, start, end):
    """
    Search for a gene in a refFlat.txt file based on coordinates.

    Parameters:
        refFlat_file (str): path to the refFlat.txt file
        chrom (str): chromosome name (e.g. 'chr1')
        start (int): start coordinate of the gene
        end (int): end coordinate of the gene

    Returns:
        gene_name (str): the name of the gene if found, None otherwise
    """
    index = create_index(refFlat_file)
    return_list = []
    if chrom not in index:
        return return_list
    genes = index[chrom]
    left = bisect_left(genes, (start, 0, ''))
    right = bisect_right(genes, (end, 0, ''))
    for i in range(left, right):
        if genes[i][0] <= end and genes[i][1] >= start:
            return_list.append(genes[i][2])
    return return_list


def hemato_gene_search(jsh_database, target_gene_list):
    gene_list = []
    with open(jsh_database, 'rt') as f:
        for line in f:
            fields = line.rstrip().split('\t')
            gene = fields[0]
            if gene not in gene_list:
                gene_list.append(gene)

    return_list = []

    for gene in target_gene_list:
        if gene in gene_list and gene not in return_list:
            return_list.append(gene)
        else:
            continue

    return return_list


def create_cnv_list(file):
    with open(file, 'rt') as input:
        return_list = []
        header_line = input.readline()
        for line in input:

            line_list = line.rstrip().split('\t')
            return_list.append(line_list[1])
            return_list.append(line_list[2])

        return_list = list(set(return_list))
        print(f'return_list = {return_list}')
        return return_list


def main():
    #
    # Argument Parse
    #
    print('cnv start')
    global myself
    argvs = sys.argv
    myself = argvs[0]
    argc = len(argvs)

    parser = argparse.ArgumentParser(description="Test program")
    parser.add_argument('-i', '--input', help="input_cnv",
                        type=str, required=True)
    parser.add_argument('-o', '--output', help="output_cnv",
                        type=str, required=True)
    parser.add_argument('-r', '--refflat', help="refflat",
                        type=str, required=True)
    parser.add_argument('-c', '--cnv_database',
                        help="cnv_database", type=str, required=True)

    arg = parser.parse_args()

    cnv_database = create_cnv_list(arg.cnv_database)

    refflat = arg.refflat
    print(arg.input)
    with open(arg.input, 'rt') as input, open(arg.output, 'wt') as output:

        header_line = input.readline()
        header_list = header_line.rstrip('\n').replace(
            '"', '').replace("'", "").split(',')
        write_buffer = '\t'.join(header_list) + '\t' + 'gene' + '\n'
        print(write_buffer)
        output.write(write_buffer)
        input.readline()
        input.readline()
        input.readline()

        for line in input:
            line = line.rstrip()
            event = line.split(',')
            chr = event[1]
            start = convert_to_int(event[10])
            end = convert_to_int(event[11])
            total_allele = convert_to_int(event[13])
            minor_allele = convert_to_int(event[14])
            if total_allele == None or minor_allele == None:
                continue
            if int(total_allele) == 2 and int(minor_allele) == 1:
                continue
            else:

                start_new = max(start - 1000000, 0)
                end_new = end + 1000000
                refflat_list = search_gene(refflat, chr, start_new, end_new)
                cnv_list = []
                for gene in refflat_list:
                    if gene in cnv_database:
                        cnv_list.append(gene)
                cnv_list = list(set(cnv_list))
                if cnv_list != []:
                    print(cnv_list)
                    write_buffer = '\t'.join(event+['hemato'])
                    write_buffer += '\t'
                    write_buffer += ','.join(cnv_list)
                    write_buffer += '\n'
                    output.write(write_buffer)


if __name__ == "__main__":
    main()
