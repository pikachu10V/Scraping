##########################################################
# pythonでは、こんな風にシャープを打つとコメントを入力できる
# コメントはプログラムに無視されるから、何を書いてもOK
# プログラムに何かコメントやメモを残したいときは、コメントアウトを使う。
##########################################################

import sys # システムを制御する
import numpy as np # 数字を扱う
import pandas as pd # データを扱う
from requests_html import HTMLSession # ウェブページを扱う
import csv # csvファイルを扱う

# import ○○ で、ほかの人が作ってくれた、すでに出来上がっているpythonのツールを呼び出す
# たとえば、pandas はデータを解析するためのライブラリ
# いちいち pandas と打つのがめんどいから、as pd で短くしている。pd.○○みたいな感じで呼び出す。

##########################################################
# 競馬の開催日付を取得する
##########################################################

str_target = "kaisai_date"
str_url_prefix = "https://race.netkeiba.com/top/calendar.html?year="

def get_race_dates(year, month):
    ScrapingSession = HTMLSession()

    # str() は、数字を文字に変換する
    # 文字 + 文字 で文字をつなげる効果がある
    # 文字 + 数字 にするとエラーが出る
    str_url = str_url_prefix + str(year) + "&month=" + str(month)

    # スクレイピング実行
    ScrapingGetHtmlResponse = ScrapingSession.get(str_url)

    # ウェブページにあるリンクをすべて取得する
    set_link = ScrapingGetHtmlResponse.html.links
    
    # "kaisai_date"を含むリンクを抽出（ここに開催日時の情報が入ってる！）
    # ブラウザで右クリック→検証 を押してちまちま探していけば、狙ってるリンクの規則性を見つけられるはず
    list_link_target = [x for x in set_link if str_target in x] # 訳: もし str_target, すなわち "kaisai_date"が名前に入っているなら抽出
    
    # 日付の抽出
    # リンクの後ろ8桁が日付になっているので、8桁だけ抽出する。
    list_str_yyyymmdd = []
    for link in list_link_target:
        list_str_yyyymmdd.append(link[-8:])

    return list_str_yyyymmdd


#  
# list_str_yyyymmdd = get_race_dates(2021,5)

# 上のコードを動かしてみる

date_start = 2019 # 取得したい年（最初）
date_end = 2021 # 取得したい年（最後）

np_date = np.arange(date_start, date_end + 1) # 2012,2013,2014,...,2021 みたいなリストを作る
np_month = np.arange(1,13) # 1,2,3,...,12 みたいなリストを作る。13にしたのは、13の一つ手前まで作られるから。

list2d_str_yyyymmdd = []
for date in np_date: # 2012,2013,2014,...,2021 の中身を一つずつ取り出す
    for month in np_month:
        print(date, month) # コンソールに出力。確認用消してもいい。
        
        try: # やってみる
            list2d_str_yyyymmdd.append(get_race_dates(date, month))
        except: # エラーが出たら無視して次に行く（これがないと、エラーが出たときにプログラムが止まる）
            print("Error: data was not found")

        #sys.sleep(1) # コメントアウトを外すと1秒待機。せっかちなのでコメントアウト。

list_str_yyyymmdd = sum(list2d_str_yyyymmdd, [])


# ファイルに日付を保存
filepath = "" #"output/" # たとえば、output フォルダに保存したい場合はこのように書く
filename_csv = "studentgrades.csv"

df_list = pd.DataFrame(list_str_yyyymmdd, columns=["date"])
df_list.to_csv(filepath + filename_csv, index=False)


print("Done") # プログラム終了確認用。消しても大丈夫
