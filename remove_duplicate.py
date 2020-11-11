import os
import sys
import argparse
import pandas as pd

def search_and_remove_duplicate(df):
    # 遺伝子名(0行目)に重複があるものだけのlistをつくる
    subdf = df[df[0].duplicated()]
    # 重複がある遺伝子の一番上の遺伝子名を抽出
    gene = subdf.iloc[0,0]
    # 指定した遺伝子のindexを取得
    dupdf = df[df[0]== gene]
    gene_indexes = list(dupdf.index)
    # <gene_name>_1, <gene_neme>_2 ...の形にして重複をなくす
    for i, gene_index in enumerate(gene_indexes):
        l = i + 1
        newname = str(gene) + "_" + str(l)
        df.iloc[gene_index, 0] = newname
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="remove duplicate")
    parser.add_argument("filename" ,help="file path", type=str)
    parser.add_argument("-n","--newfile", help="new file name", type=str, default="remove_duplicate.csv")

    args = parser.parse_args()

    path = args.filename
    newfile = args.newfile

df = pd.read_table(path, header=None)

#anyはTrueが1つでもあればTrue。重複がなくなるまでループ
while any(df[0].duplicated()):
    df = search_and_remove_duplicate(df)

else:
    df.to_csv(newfile, header=False, index=False)
