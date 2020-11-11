import os
import sys
import argparse
import pandas as pd

# Ensemblの方のデータにはheaderがないのでNoneにした
# UCSCのデータを適用するとheaderの関係でcautionが出てくるが動作はする
def read_file(path):
    df = pd.read_table(path, header=None)
    return df

# NIPBLはUCSCの方では2つ、Ensemblの方では1つ
# 複数ある場合のために、geneIDをkeyにしてexonStartsとexonEndsの値を各々dict型で保存
def create_strand_list(sub_df):
    starts_dict = {}
    ends_dict = {}
    
    for n in range(len(sub_df)):

        name = sub_df.iloc[n,1]
        # exonStarts(9行目)の値をリストにする
        starts = sub_df[9].iloc[n]
        # ","で区切らないと[17914, 18267]を[1,7,9...,6,7]という風に認識してしまう
        starts = list(starts.split(","))
        
        #gine: pop()することで最後の空の要素を除きました。
        starts.pop()
        # geneIDをkeyにexonStartsのlistをvalueに保存
        starts_dict[name] = starts

        #　exonEnds(10行目)についても同様
        ends =  sub_df[10].iloc[n]
        ends = list(ends.split(","))
        ends.pop()
        ends_dict[name] = ends
        
    return starts_dict, ends_dict

# 作成した辞書の値を出力する
def extract_start_end(divided_df, directions, newfile, gene):
    # "a" : textの最後に文字を追加する
    newtext = open(newfile, "a", encoding="utf-8")
    
    if any(df[0] == gene):
        starts_dict, ends_dict = create_strand_list(divided_df)
    
        for key, values in starts_dict.items():
            print("gene ID : " + str(key))
            newtext.write("gene ID : " + str(key) + "\n")

            #gina: 結果でstart-endの位置をよりわかりやすくするためにゲノムでの方向を示しました。
            newtext.write("direction : " + str(directions) + "\n")

            starts_list = starts_dict[key]
            ends_list = ends_dict[key]
            
            # Ensemblのときはこのままで大丈夫
            # UCSCがstartとendsが逆になってない
            # UCSCのときは逆順にしなくていいのでlistのlをiに書き換える(もっと良い方法ありそう)
            for i in range(len(starts_list)):
                # starndが"-"の時は後ろからの出力にする
                if directions == "-":
                    l = -(i + 1)

                    #gina: ここまでやる必要はないかもしれませんが、"-"のときは、start-endが
                    #      数の大きいほう-数の小さいほうとなるようにしました。
                    #gine: リストをソートすることで、元ファイルの並びを一律にしました。
                    start = sorted(ends_list)[l]
                    end = sorted(starts_list)[l]
                    
                else:
                    l = i
                    
                    #gine: リストをソートすることで、元ファイルの並びを一律にしました。
                    start = sorted(starts_list)[l]
                    end = sorted(ends_list)[l]
                print(str(start) + "-" + str(end))
                newtext.write(str(start) + "-" + str(end)+"\n") 
        newtext.close()
    
    return newtext

def devide_forward_reverse(df, newfile, gene):
    # strand(3番目)がforward(+)かreverse(-)かで分ける
    posi_df = df[df[3] == "+"]
    nega_df = df[df[3] == "-"]
    extract_start_end(posi_df, "+", newfile, gene)
    extract_start_end(nega_df, "-", newfile, gene)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract first end")
    parser.add_argument("filename" ,help="file path", type=str)
    parser.add_argument("genename", help="genename or ID", type=str)
    parser.add_argument("-n","--newfile", help="new file name", type=str, default="start_end.txt")

    args = parser.parse_args()

    path = args.filename
    gene = args.genename
    newfile = args.newfile
    
# 0行目の遺伝子名、1行目の遺伝子IDの両方で検索可能
df = read_file(path)

print(str(gene) + ":" + "start - end")

# 遺伝子名がファイル内に存在しているか確認
if any(df[0] == gene):
    df = df[df[0] == gene]
    devide_forward_reverse(df, newfile, gene)

elif any(df[1] == gene):
    df = df[df[1] == gene]
    devide_forward_reverse(df, newfile, gene)

else:
    print("ERR : There is no input gene in input file")
