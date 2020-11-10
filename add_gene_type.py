import os
import sys
import argparse
import pandas as pd

# 共通遺伝子名のリスト作成
def extract_common_gene_list(ucsc, ensembl):
    ucsc_df = pd.read_table(ucsc)
    ensembl_df = pd.read_table(ensembl, header=None)
    set1 = set(ucsc_df["#geneName"])
    set2 = set(ensembl_df[0])
    common_gene = set1 & set2
    common_list = list(common_gene)

    return ucsc_df, ensembl_df, common_list

# ucscのファイル(hg38の方)の最後の列にgene_typeの列を追加する
def add_genetype(ucsc_df, ensembl_df, common_list):
    # ensembl(GRCh38の方)で共通遺伝子リストに遺伝子が含まれているデータのみを抽出する
    df = ensembl_df[ensembl_df[0].isin(common_list)]
    # 遺伝子名(0行目),gene_type名(12行目)を各々listにする
    gene_names = list(df[0])
    gene_types = list(df[12])
    
    for i in range(len(df)):
        gene_name = str(gene_names[i])
        gene_type = str(gene_types[i])
        # ucscのデータで遺伝子名の一致がある列の最後にgene_typeを追加する
        ucsc_df.loc[ucsc_df["#geneName"] == gene_name, "gene_type"] = gene_type
    return ucsc_df

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="add common gene type to UCFC file")
    parser.add_argument("ucsc" ,help="input UCSC file", type=str)
    parser.add_argument("ensembl" ,help="input Ensembl file", type=str)
    parser.add_argument("-n","--newfile", help="new file name", type=str, default="add_gene_type.csv")

    args = parser.parse_args()

    ucsc = args.ucsc
    ensembl = args.ensembl
    newfile = args.newfile

ucsc_df, ensembl_df, common_list = extract_common_gene_list(ucsc, ensembl)
ucsc_df = add_genetype(ucsc_df, ensembl_df, common_list)
# csvファイルに出力する
ucsc_df.to_csv(newfile, header=True, index=False)

