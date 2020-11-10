import os
import sys
import argparse
import pandas as pd

# dataframeの遺伝子名(0行目)をset型にする
def make_set(first, second):
    df1 = pd.read_table(first, header=None)
    df2 = pd.read_table(second, header=None)
    set1 = set(df1[0])
    set2 = set(df2[0])
    
    # どちらかのファイルに#geneNameが入っているので除去
    if "#geneName" in set1:
        set1.discard("#geneName")
    elif "#geneName" in set2:
        set2.discard("#geneName")

    return set1, set2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract common and non-common gene")
    parser.add_argument("first_file" ,help="file path", type=str)
    parser.add_argument("second_file" ,help="file path", type=str)

    args = parser.parse_args()

    first = args.first_file
    second = args.second_file

set1, set2 = make_set(first, second)
# & 共通部分
common_gene = set1 & set2
# ^ 対称差集合（二つの集合のどちらか一方にのみ含まれる要素の集合）
non_common_gene = set1 ^ set2

print("between" + str(first) + "and" + str(second))
print("the number of common is " + str(len(common_gene)))
print("the number of difference is " + str(len(non_common_gene)))