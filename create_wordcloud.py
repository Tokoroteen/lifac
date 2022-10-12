import pandas as pd
from wordcloud import WordCloud

def create_wordcloud(name, df):
    #fontの指定
    # font = 'ヒラギノ角ゴシック W3.ttc'
    font = '/app/.fonts/ipaexg.ttf'

    #nameのインデックス番号
    i = df.loc[df['name']==name].index[0]
    #アクティビティーNo.
    n = df['No.'].iloc[i]

    wordcloud = WordCloud(font_path=font,
    mode = 'RGBA', background_color='rgba(255, 255, 255, 0)', #transparent
    width = 800,
    height = 600,
    max_words=120,
    stopwords=['の','する', 'いる', 'ある','なる','体験','できる','こと','良い','いただく','方','思う']
    )

    wordcloud.generate(df['wakati_kihon_str'].iloc[i])
    wordcloud.to_file(f"./static/wordcloud/{n}.png")
    return n #アクティビティーNo.を返す