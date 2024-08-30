#pysamを利用して,a.csvにはあるが、b.csvにはないSNPについて、c.bamから該当するリードを抽出し、塩基の頻度を求めるimport pysam
import csv
import pysam

# a.csvとb.csvを読み込み、a.csvにあってb.csvにないSNPのリストを作成する
with open('a.csv', 'r') as a_file, open('b.csv', 'r') as b_file:
    a_reader = csv.reader(a_file)
    b_reader = csv.reader(b_file)
    a_snps = set(row[0] for row in a_reader)
    b_snps = set(row[0] for row in b_reader)
    snps = a_snps - b_snps

# c.bamをpysamで読み込む
bamfile = pysam.AlignmentFile("example.bam", "rb")

# SNPリストに対して、pysamを使用してc.bamから該当するリードを抽出する
for snp in snps:
    for pileupcolumn in bamfile.pileup(snp, max_depth=100000):
        if pileupcolumn.pos == snp:
            for pileupread in pileupcolumn.pileups:
                if not pileupread.is_del and not pileupread.is_refskip:
                    # TODO: SNPの塩基の頻度を求める

# pysamで読み込んだbamファイルを閉じる
bamfile.close()