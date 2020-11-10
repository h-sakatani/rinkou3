# 遺伝子タイプと言っているので入力はrefFlat.GRCh38.gene.name.txtのはず
import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# 遺伝子のタイプごとにexon数をカウント→合計する??
# 遺伝子のタイプごとのexon数の合計(sum)をヒストグラムにする??
# $ python3 count_exon.py refFlat.GRCh38.gene.name.txt -n sum.png
# もしくは
# 遺伝子のタイプごと(each)にヒストグラムを作成する??
# python3 count_exon.py refFlat.GRCh38.gene.name.txt -o each     

def sum_of_each_type(df, newfile):
    # 遺伝子タイプ(12番目)ごとに各値を合計する
    df1 = df.groupby(12).sum()
    # exon count(8番目)の合計
    plt.figure(figsize=(10, 10))
    plt.hist(df1[8])
    plt.title("The number of exon", fontsize = 15)
    plt.xticks(rotation=70)
    plt.xlabel("range of exon count", fontsize = 12)
    plt.ylabel("frequency", fontsize = 12)
    plt.savefig(newfile)

def histgram_of_each_type(df, newfile):
    # 遺伝子タイプ(12番目)ごとのexon_count(8番目)の各ヒストグラムを作成する
    df[8].hist(by=df[12], figsize=(25,20))
    plt.tight_layout()
    plt.savefig(newfile)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create exon count histgram")
    parser.add_argument("filename" ,help="file path", type=str)
    parser.add_argument("-n","--newfile", help="new file name", type=str, default="new_histgram.png")
    parser.add_argument("-o","--option", help="sum or each", type=str, default="sum")

    args = parser.parse_args()

    path = args.filename
    newfile = args.newfile
    option = args.option


df = pd.read_table(path, header=None)

if option == "sum":
    sum_of_each_type(df, newfile)
elif option == "each":
    histgram_of_each_type(df, newfile)
else:
    print("ERR : select correct option")