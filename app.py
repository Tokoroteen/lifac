from cmath import pi
import pandas as pd
import random
from flask import Flask, render_template, request, flash
import model
from create_wordcloud import create_wordcloud

app = Flask(__name__, static_folder='./static')

#シークレットキー
app.secret_key="\xf6\xcc\xfa\xa3\x83\xc3\xe9\xfd\x83\xe8"

search = model.Search()
image = model.Image()

#base_data
df_base = pd.read_csv('base_data.csv')

#wordcloud用のcsv
df_wordcloud = pd.read_csv('wordcloud.csv')

#最初のページ
@app.route('/', methods=["GET"])
def index():
    #ヒントを選ぶ
    example_list=['彼女との思い出に残る記念日','山で思いっきりはしゃぎたい','ストレスを解消したい','とにかくリラックスして体を休めたい','空を飛ぶ','美味しいものをおなかいっぱい食べたい','非日常感あふれる体験をしたい','カップルの記念日','海でできる楽しいこと','山でできるワクワクすること','川でのアクティビティー','日本文化を味わいたい','動物に癒される']
    example=random.choice(example_list)
    return render_template('index.html', example=example)

    # elif request.method == "POST":
    #     input_text = request.form["input_text"]
    #     print(input_text)
    #     return render_template('index.html')

#結果を表示する
@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        input_text = request.form["input_text"]

        try: #結果を返す
            #a_nameがアクティビティーの名前／a_scoreが類似度
            a_name, a_score = search.activ_search(input_text) #search activity
            #a_nameのジャンルとリンク
            a_genre = df_base[df_base['name']==a_name]['genre_type']
            a_genre = str(a_genre.values).replace(' ','').replace('"','').replace("'","").replace("[","").replace("]","")
            a_link = df_base[df_base['name']==a_name]['url']
            a_link = a_link.values[0]
            #wordcloudをつくる
            n = create_wordcloud(a_name, df_wordcloud)
            img = f'static/wordcloud/{n}.png'
            return render_template('result.html', input_text=input_text, activity=a_name, score=a_score, image=img, genre=a_genre, link=a_link)

        except ValueError as v: #値が不当な時の処理
            flash('1つ以上の名詞や動詞を入力してください')
            return render_template('index.html')


    elif request.method == "GET":
        return render_template('result.html', input_text='None', activity='値が存在しません')

#結果を修正する
@app.route('/fix', methods=["POST"])
def fix():
    # if request.method == "POST":
    #hiddenの要素
    input_text = request.form["input_text"]
    a_name = request.form['activity']
    a_score = request.form['score']
    img = request.form['img']

    positive_text = request.form["positive_text"]
    negative_text = request.form["negative_text"]
    print(positive_text, 'and', negative_text)
    print(positive_text)

    if positive_text == '' and negative_text == '': #両方とも空欄だったら
        flash('追加したい要素、削除したい要素の両方、またはいずれかを入力してください')
        return render_template('result.html', input_text=input_text, activity=a_name, score=a_score, image=img)

    elif negative_text=='': #negative_textだけが空欄だったら
        a_name, a_score = search.activ_fix(input_text ,positive_text, negative_text) #search activity
        #wordcloudをつくる
        n = create_wordcloud(a_name, df_wordcloud)
        img = f'static/wordcloud/{n}.png'
        equation = f'{input_text} + {positive_text}'
        return render_template('result.html', input_text=equation, activity=a_name, score=a_score, image=img)

    elif positive_text == '': #positive_textだけが空欄だったら
        a_name, a_score = search.activ_fix(input_text ,positive_text, negative_text) #search activity
        #wordcloudをつくる
        n = create_wordcloud(a_name, df_wordcloud)
        img = f'static/wordcloud/{n}.png'
        equation = f'{input_text} - {negative_text}'
        return render_template('result.html', input_text=equation, activity=a_name, score=a_score, image=img)

    else: #どちらも入力されたら
        a_name, a_score = search.activ_fix(input_text ,positive_text, negative_text) #search activity
        #wordcloudをつくる
        n = create_wordcloud(a_name, df_wordcloud)
        img = f'static/wordcloud/{n}.png'
        equation = f'{input_text} + {positive_text} - {negative_text}'
        return render_template('result.html', input_text=equation, activity=a_name, score=a_score, image=img)

    # elif request.method == "GET":
    #     return render_template('result.html', activity='値が存在しません')

#説明ページ
@app.route('/detail', methods=["GET"])
def detail():
    return render_template('detail.html')

if __name__ == "__main__":
    app.run(debug=True)