import pandas as pd
import calendar

# ファイルパス
file_path = 'chibakidscafelist.csv'

#ここにお気に入りにしたい「こども食堂の名称」を書き込んでください
MY_FAVORITES = [
    "マルちゃん食堂",
    "まんぷく食堂",
    "かがやきっ子食堂",
    "TSUGA no わ こども食堂",
    "地域食堂まさご" # 新しく追加
]

try:
    # CSVファイルを読み込む
    df = pd.read_csv(file_path)

    #  お気に入り情報をCSVに反映 
    df['favorite'] = 0
    df.loc[df['こども食堂の名称'].isin(MY_FAVORITES), 'favorite'] = 1
    
    # お気に入りだけを抽出 
    favorites_df = df[df['favorite'] == 1].copy()

    if favorites_df.empty:
        print("お気に入りに登録された開催情報がありません。")
    else:
        # 'date' カラムをdatetime型に変換
        favorites_df['date'] = pd.to_datetime(favorites_df['date'], errors='coerce')
        favorites_df.dropna(subset=['date'], inplace=True)

        # 表示するカレンダーの年と月（データに合わせて2025年9月を指定）
        year = 2025
        month = 9

        print(f"{year}年{month}月のお気に入りカレンダー ")
        print("月 火 水 木 金 土 日")

        # その月に開催されるお気に入りの食堂情報を抽出
        month_events = favorites_df[
            (favorites_df['date'].dt.year == year) &
            (favorites_df['date'].dt.month == month)
        ]

        cal = calendar.monthcalendar(year, month)

        # カレンダーに開催日を表示
        for week in cal:
            week_str = ""
            for day in week:
                if day == 0:
                    week_str += "   "
                else:
                    if day in month_events['date'].dt.day.values:
                        week_str += f"{day:2}* "
                    else:
                        week_str += f"{day:2}  "
            print(week_str)

        print("\n お気に入りの開催情報一覧")
        if not month_events.empty:
            # 日付でソートして、名称と所在地を表示
            for index, row in month_events.sort_values('date').iterrows():
                print(f"【{row['date'].strftime('%Y-%m-%d')}】 {row['こども食堂の名称']}")
                print(f"   └ 場所: {row['所在地']}")
        else:
            print(f"{year}年{month}月にお気に入りの開催情報はありません。")


except FileNotFoundError:
    print(f"エラー: ファイル '{file_path}' が見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")