library(tidyverse)
library(readxl)
library(BSgenome.Hsapiens.UCSC.hg19)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(org.Hs.eg.db)
library(TCGAbiolinks)
options(repos = c(CRAN = "https://cran.ism.ac.jp/"))

setwd("/Users/fukushimahideto/Desktop/clinical_sequencing_workflow")


###############################################
# メインの関数＝annotate-mutationの定義


annotate_mutations <- function(mut_file) {
  ref_genome <- BSgenome.Hsapiens.UCSC.hg19
  txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
  genes_hg19 <- genes(TxDb.Hsapiens.UCSC.hg19.knownGene)

  mut_pt <- read_tsv(mut_file)

  for (r in 1:length(mut_pt$Start)) {
    if (mut_pt$Ref[r] == "-") {
      mut_pt$Start[r] <- mut_pt$Start[r] + 1
      mut_pt$End[r] <- mut_pt$Start[r]
      insert <- getSeq(ref_genome, paste0("chr", mut_pt$Chr[r]), start = mut_pt$Start[r], end = mut_pt$End[r])[1]
      mut_pt$Ref[r] <- as.character(insert)
      mut_pt$Alt[r] <- paste0(insert, mut_pt$Alt[r])
    }
  }

  mut_pt$End <- mut_pt$Start

  mut_pt$mutID <- paste(mut_pt$Chr, mut_pt$Start, mut_pt$End, mut_pt$Ref, mut_pt$Alt, sep = "_")

  AML <- read_csv("miscellaneous/AML2022.csv")
  MPN <- read_csv("miscellaneous/MPN2018.csv")
  nanya <- read_csv("miscellaneous/nanya_sig.csv")
  DLBCL <- read_csv("miscellaneous/DLBCL_2018.csv")
  Germline_JSH <- read_tsv("new_annotation_list/jsh_germline.tsv")
  Germline_ACMG <- read_tsv("new_annotation_list/AGMC_V3_1.tsv")
  shizuoka <- read_csv("miscellaneous/shizuoka.csv")
  hiden_no_tare <- read_tsv("new_annotation_list/hg19_COSMIC98hem_converted.tsv")
  jsh_trunc <- read_tsv("new_annotation_list/jsh_trunc.tsv")

  mut_pt <- left_join(mut_pt, nanya, by = "mutID")
  mut_pt <- left_join(mut_pt, AML, by = "mutID")
  mut_pt <- left_join(mut_pt, MPN, by = "mutID")
  mut_pt <- left_join(mut_pt, DLBCL, by = "mutID")
  mut_pt <- left_join(mut_pt, shizuoka, by = "Gene.refGene")
  mut_pt <- left_join(mut_pt, Germline_JSH, by = "Gene.refGene")
  mut_pt <- left_join(mut_pt, Germline_ACMG, by = "Gene.refGene")
  mut_pt <- left_join(mut_pt, hiden_no_tare, by = "mutID")
  mut_pt <- left_join(mut_pt, jsh_trunc, by = "Gene.refGene")


  return(mut_pt)
}

###################################################
# main()
args <- commandArgs(trailingOnly = T)
sample_path <- args[1]
mut_pt <- annotate_mutations(sample_path)

# cosmic98_HemDisease列は、""に内包されているので、これを削除"
# "acute_myeloid_leukaemia:1, chronic_myeloid_leukaemia:1"
# そしてそれを、分割する（要改善）
mut_pt$cosmic98_HemDisease <- gsub('"', "", mut_pt$cosmic98_HemDisease)
mut_original <- mut_pt %>%
  extract(cosmic98_HemDisease, into = c("disease_rest1", "disease_type1", "number1"), regex = "(.*),(.*):(.*)") %>%
  extract(disease_rest1, into = c("disease_rest2", "disease_type2", "number2"), regex = "(.*),(.*):(.*)") %>%
  extract(disease_rest2, into = c("disease_rest3", "disease_type3", "number3"), regex = "(.*),(.*):(.*)") %>%
  extract(disease_rest3, into = c("disease_rest4", "disease_type4", "number4"), regex = "(.*),(.*):(.*)") %>%
  extract(disease_rest4, into = c("disease_rest5", "disease_type5", "number5"), regex = "(.*),(.*):(.*)")

write_tsv(mut_original, gsub(".tsv", "original_anno.tsv", sample_path))

# ここからが抽出
# 1 mut_original から　cosmicの登録数が5個以上に渡るものを抽出する、あるいは5疾患以上において登録のあるものを抽出し、それをmut_cosmicとする。 output_file = gsub(".tsv", "cosmic_anno.tsv", sample_path)
mut_cosmic <- mut_original %>% filter(cosmic98_HemNum >= 10 | number1 >= 5 | number2 >= 5 | number3 >= 5 | number4 >= 5 | number5 != NA)
write_tsv(mut_cosmic, gsub(".tsv", "cosmic_anno.tsv", sample_path))

# 2 truncating mutationのリストを取ってくる
mut_trunc <- mut_original %>% filter(ExonicFunc.refGene == "frameshift deletion" | ExonicFunc.refGene == "frameshift insertion"| ExonicFunc.refGene == "stopgain" | ExonicFunc.refGene == "stoploss" | Func.refGene == "splicing") %>% filter(jsh_trunc == 1)
write_tsv(mut_trunc, gsub(".tsv", "trunc_anno.tsv", sample_path))



# 3 germline のリストに合致するものを抽出する

mut_germline <- mut_original %>% filter(acmg == 1 | jsh_germline == 1)
write_tsv(mut_germline, gsub(".tsv", "germline_anno.tsv", sample_path))
