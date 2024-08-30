library(tidyverse)
library(biomaRt)
library(httr)

JSH_driver <- read_csv("genelist_JSH.csv")
JSH_driver <- JSH_driver$genelist_JSH

set_config(config(timeout = 150))

# Ensemblデータベースにアクセスするためのオブジェクトを作成
ensembl <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")

# 任意の染色体番号と塩基番号の領域を設定
chromosome <- "5"  # 染色体番号
start_position <- 172517318	# 開始塩基番号
end_position <- 178540868# 終了塩基番号

#1000000塩基のマージをつける
start_position <- start_position - 1000000
end_position <- end_position + 1000000

# startpositionが0より小さい場合、0に設定
start_position <- max(start_position, 0)

# 指定した領域に含まれる遺伝子を取得
genes <- getBM(attributes = c("hgnc_symbol"),
               filters = c("chromosome_name", "start", "end"),
               values = list(chromosome, start_position, end_position),
               mart = ensembl)

# 遺伝子名をベクトルに代入
gene_names <- genes$hgnc_symbol

# ベクトルの内容を表示
print(gene_names)

# gene_namesから一致する要素を抽出
driver_genes <- gene_names[gene_names %in% JSH_driver]

# 結果を表示
print(driver_genes)

