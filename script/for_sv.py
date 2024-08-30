import os
import sys
import argparse


def create_sv_list(file):
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

#
# Main
#
def main():
    #
    # Argument Parse
    #

    global myself
    argvs = sys.argv
    myself = argvs[0]
    argc = len(argvs)

    parser = argparse.ArgumentParser(description="Test program")
    parser.add_argument(
        "-i1", "--input1", help="input1_sv_self", type=str, required=True
    )
    parser.add_argument(
        "-i2", "--input2", help="input2_sv_other", type=str, required=True
    )
    parser.add_argument("-o", "--output", help="output_sv", type=str, required=False)
    parser.add_argument("-s", "--sv_database", help="sv_database", type=str, required=False)

    arg = parser.parse_args()
    
    sv_database = create_sv_list(arg.sv_database)
    
    annotation_list = []
    filtered_list = []
    with open(arg.output, "wt") as output, open(arg.input1, "rt") as input1, open(
        arg.input2, "rt"
    ) as input2:
        output.write(
            "Chr_1\tPos_1\tDir_1\tChr_2\tPos_2\tDir_2\tInserted_Seq\tVariant_Type\tGene_1\tGene_2\tExon_1\tExon_2\tNum_Tumor_Ref_Read_Pair\tNum_Tumor_Var_Read_Pair\tTumor_VAF\tNum_Control_Ref_Read_Pair\tNum_Control_Var_Read_Pair\tControl_VAF\tMinus_Log_Fisher_P_value\tNon-Matched_Control_Sample_With_Max_Junction\tNum_Max_Non-Matched_Control_Junction\tMax_Over_Hang_1\tMax_Over_Hang_2\n"
        )


        for line in input1:
            line = line.rstrip()
            if line.startswith("#"):
                continue
            if line.startswith("Chr_1"):
                continue
            event = line.split("\t")
            print(event)
            Gene_1, Gene_2 = event[8], event[9]
            overhang_1, overhang_2 = event[21], event[22]
            if Gene_1 in sv_database or Gene_2 in sv_database:
                if int(overhang_1) > 100 and int(overhang_2) > 100:
                    output.write(line + "\n")
            # if int(overhang_1) > 100 and int(overhang_2) > 100:
            #     output.write(line + "\n")
                

        for line in input2:
            line = line.rstrip()
            if line.startswith("#"):
                continue
            if line.startswith("Chr_1"):
                continue
            event = line.split("\t")
            print(event)
            Gene_1, Gene_2 = event[8], event[9]
            overhang_1, overhang_2 = event[21], event[22]
            if Gene_1 in sv_database or Gene_2 in sv_database:
                if int(overhang_1) > 100 and int(overhang_2) > 100:
                    output.write(line + "\n")
            # if int(overhang_1) > 100 and int(overhang_2) > 100:
            #     output.write(line + "\n")


if __name__ == "__main__":
    main()
