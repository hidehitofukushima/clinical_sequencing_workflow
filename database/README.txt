
################################
CLINICAT
Made by:Hidehito Fukushima 
Date:2023/09/27
################################

【環境】
@python3.11.4





【目次】

・前半：CLINICATの使用方法
1 インストール
2 cd {clinical_sequencing_workflowをインストールしたディレクトリ}
3 Rを起動 
4 renv::init() 
5 Rを終了
6 master_snv.sh

・後半：クリニカルシーケンスのプロトコール（共通版）＋抽出アルゴリズムについて

todo: sv,CNVのワークフローも統一して、複数のファイルを全部入力にして一発実行できるようにする
todo: html/revealjsによるレポート作成
###############################

SNV 実行時間約３分

preparation: master_snv.shの中のinput1/input2にそれぞれ、v6.1でコールした全体ファイル・他人対照でv6.1でコールした全体ファイルのパスを入力
Command: cd {clinical_sequencing_workflowをインストールしたディレクトリ} && ./master_snv.sh
explanation:
for_snv.sh: 
    input: v6.1で出力されたsomatic/allファイルの2つ
    output: CLNVARで「Pathogenic」あるいは「Likely-pathogenic」となったsnvレコード。列数は402->必要なもののみへ。変更は簡単に可能。
    example_script:master.sh
    point:もともとの巨大なyokomon_outputファイルを、mycに限らず一気に処理する。Rやpythonではメモリの関係で動かないため、shellscriptで処理。

for_snv.R:
    input: sor_snv.shのoutput
    output: さらに、cosmicの造血器腫瘍で登録が何件あるかのアノテーションデータを付加し、nullでないところのみを抽出した
    
################################

SVの手順


################################

レポート作成の手順


################################
【追加のフィルタリングアイデア】
例：MYC1:
①nonsynonimous な
変異でJSHの登録内容、COSMICの登録内容が疾患と関連のあるものを拾いigvで確からしいか確認する。 それぞれの遺伝子について、機能獲得型変異をきたすのか喪失型変異を来すのかをJSHのdatabaseで確認する。獲得型はCOSMICの登録がない変異はほぼVUS, 喪失型はCOSMICの登録がない場合でも疾患関連性が疑われるので保留。SHIFTやPolyphen2の値、Clinvar Minerでの登録の有無を検索し、病原性があるかどうかを検討する。
②frame shift変異はigvでframe shiftの内容を確認し、COSMICで同じ位置や近傍に同様の変異がないかサイトで確認する。
③stopgainは該当遺伝子について、JSHでの登録内容、COSMICで類似のstopをきたす変異がないかを確認する。
MYC2以下は、JSHのガイドラインに登録のある遺伝子のみを抽出し、その中で、snp 131 nonflaggedに上がらないものを抽出。残りの遺伝子をMYC1と同様に確認する。
 

【クリニカルシーケンスのプロトコール】
コール結果→
clinicatで遺伝子を抽出→
igvスナップショット作成→
過去のデータベースからアノテーションファイルを回収し、再利用→
RevealJSでレポート作成→
重要遺伝子について、レポートをひな形として再回収し、データベース化

【重要なデータベース解説】
COSMIC
CLINVAR（今回は使用せず）
造血器腫瘍ゲノム検査ガイドライン（http://www.jshem.or.jp/genomgl/home.html）
cBioPortal (https://www.cbioportal.org/)
shift, polyphen2
この辺のデータベースを一通りいじる、変異を確認する作業が必要、近傍のやつも
Tommo : アレル頻度のデータベース　cutoff= 0.01%(strict) ~ 1%(loose)


【フリー記載欄】
snvのフィルタリングのアイデア
①cosmicに登録があるからひろってくるもの：
②cosmicに登録なくても拾ってくるもの：tuncating変異（jshから拾える？）については、JSHの変異リストで機能喪失・獲得を確認、がん抑制遺伝子であれば、機能喪失を持つもののみをフィルタ
③germline：acmg+それ以外の有名な変異をリスト化⇛Tommo < 0.1%, ⇛cinsg＝pathogenic/likely-pathogenic


svのフィルタリングのアイデア
①overhang > 100 かつ、jshガイドラインに登録のあるもの

cnvのフィルタリングのアイデア
①ｊｓｈガイドラインから、増幅、欠失,ampをリスト化⇛いまあるリストをそれで置換し、該当するもののみを抽出することにする

result.filt.all = EB call後のgenomon call結果にYokomonをかけたものになります。これがfilesizeが極端に小さいはずです。
result.filt_nofilt.all.comblined
 最低限のfilter設定(フィッシャー検定+read depthとsupporting redad数)をかけただけのgenomon call結果にYokomonをかけたもの (="nofilt.all")
と
EB callをかけた結果にYokomonをかけたもの".filt.all "
の和集合(combined)です。(filt_nofilt.all.comblined )
実質、result.all.comblined=result.filt_nofilt.all.comblined のはずです。
私はresult.filt_nofilt.all.comblined を主にcurationに使用しています。germlineはresult.filt.all を使用しています。
【スクリプト・データベース置き場】







#miscellaneous 
- cnv用のスクリプト
ー　get_genelist_from_JSH.py
- get////txt
- 














