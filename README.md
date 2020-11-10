# 輪講

----

## お題1　各遺伝子について、exon領域を “start-end,start-end,…”と出力する処理を実装。NIPBLで例示。


例
 ``python3 start_end.py refFlat.hg38.txt NIPBL -n start_end.txt ``

defaltでファイル名start_end.txtが出力される<br>
NIPBLはGRCh38(Ensembl)では1つ、hg38(UCSC)では2つ存在<br>
出力ファイルの中身は、geneID、start-end 、start-end 、…　、geneID、start-end 、start-end …となる<br>
strandが"+"か"―"かによってexonStartとexonEndsの順番が変わる(これはGRCh38*のみ??)<br>

### 問題点
後で気づいたので、input dataによる修正は行っておらず'extract_start_end'のlとiをその都度入れ替えている(今のところ)<br>
遺伝子名に重複があって遺伝子IDに重複がある場合は、遺伝子IDの重複が考慮されていないので出力は分けられない<br>


## お題2　遺伝子のタイプごとにexon数をカウントし、分布をヒストグラムで表示する。

例
 ``python3 count_exon.py refFlat.GRCh38.gene.name.txt -n sum.png -o sum``

``python3 count_exon.py refFlat.GRCh38.gene.name.txt -n each.png -o each``

遺伝子のタイプごとのexon数の合計(sum)をヒストグラムにする<br>
もしくは<br>
遺伝子のタイプごと(each)にヒストグラムを作成する<br>
どちらかわからなかったので、optionでsum、eachを作成することで対応<br>

### 問題点
作成した図が合っているのか???

![sum](https://user-images.githubusercontent.com/71812107/98615289-95e93d00-233d-11eb-8495-88c33e1d0b21.png)
sum.png

![each](https://user-images.githubusercontent.com/71812107/98615341-b2857500-233d-11eb-9dca-c795352beeb2.png)
eac.png


## お題3　それぞれの遺伝子ファイルについて、「何らかの方法で」遺伝子の重複を除いた修正ファイルを作成する。

例
``python3 remove_duplicate.py refFlat.GRCh38.gene.name.txt -n remove_duplicate.csv``

重複遺伝子があったら、遺伝子名-1、遺伝子名-2、…とすることで重複をなくす<br>
defaltではremove_duplicate.csvが作成される

## お題4　２つの遺伝子ファイル間で共通する遺伝子、共通でない遺伝子がいくつ存在するかカウントする。

例
``python3 count_gene.py refFlat.GRCh38.gene.name.txt refFlat.hg38.txt``

ファイルの順番は逆でも良い<br>


## お題5　２つの遺伝子ファイル間で共通する遺伝子について、 refFlat.hg38.txtにgene typeの列を追加したファイルを作成する。

例
``python3 count_gene.py refFlat.GRCh38.gene.name.txt refFlat.hg38.txt``

defalutでadd_gene_type.csvを出力<br>
順番はucsc、ensemblファイルでないと作動しない(問題点??)
