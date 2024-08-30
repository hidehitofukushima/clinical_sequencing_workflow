library(dplyr)
library(readxl)
library(BSgenome.Hsapiens.UCSC.hg19)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(org.Hs.eg.db)
library(TCGAbiolinks)
library(biomaRt)


setwd("/Users/fukushimahideto/Library/Mobile Documents/com~apple~CloudDocs/clinical_sequencing/データベース/clinicalseq")


###############################################
# メインの関数＝annotate-mutationの定義
ref_genome <- BSgenome.Hsapiens.UCSC.hg19
txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
genes_hg19 <- genes(TxDb.Hsapiens.UCSC.hg19.knownGene)


 mut_pt <- read_tsv('/Users/fukushimahideto/Library/Mobile Documents/com~apple~CloudDocs/clinical_sequencing/データベース/clinicalseq/hg19_COSMIC98hem.tsv')

  for (r in 1:length(mut_pt$Start)) {
    if (mut_pt$Ref[r] == "-") {
      mut_pt$Start[r] <- mut_pt$Start[r] + 1
      mut_pt$End[r] <- mut_pt$Start[r]
      insert = getSeq(ref_genome, paste0("chr", mut_pt$Chr[r]), start = mut_pt$Start[r], end = mut_pt$End[r])[1]
      mut_pt$Ref[r] <- as.character(insert)
      mut_pt$Alt[r] <- paste0(insert, mut_pt$Alt[r])
    }
  }

  mut_pt$End <- mut_pt$Start

  mut_pt$mutID <- paste(mut_pt$Chr, mut_pt$Start, mut_pt$End, mut_pt$Ref, mut_pt$Alt, sep = "_")
  mut_pt <- mut_pt %>% dplyr::select(mutID, cosmic98_HemDisease, cosmic98_HemNum, cosmic98_PMID)

  write_tsv(mut_pt, '/Users/fukushimahideto/Library/Mobile Documents/com~apple~CloudDocs/clinical_sequencing/データベース/clinicalseq/hg19_COSMIC98hem_converted.tsv')




