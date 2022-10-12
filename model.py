#import library
import numpy as np
import pandas as pd
import pickle
from gensim.models import word2vec
import MeCab
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

#model load
model = Doc2Vec.load('./asoview_token_upto500.model')
#タグはMeCab.Tagger（neologd辞書）を使用
# tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
tagger = MeCab.Tagger()

class Search:
    def __init__(self) -> None:
        pass

    def wakati(self, query): #クエリを分かち書きする関数
        words = []
        node = tagger.parseToNode(query)
        while node:
            if node.feature.split(',')[0] in ["名詞","形容詞","形容動詞","動詞"]:#分かち書きで取得する品詞を指定
                words.append(node.surface)
            node = node.next
        return words

    def get_wv(self, words): #get word vectors from list of words
        words = self.wakati(words) #まず分かち書き
        word_vec = [] #ここに単語ベクトルをいれていく

        for word in words: #各単語ずつ
            try:
                word_vec.append(model.wv[word]) #search word_vector in words
            # word_vec = model.infer_vector(wakati(words))

            except KeyError as k: #when the words are not in the vocablary
                print(k)
                word_vec.append(model.infer_vector([word]))

        return word_vec

    def activ_search(self, words):
        word_vec = self.get_wv(words)
        activ_list = model.dv.most_similar(positive=word_vec) #list of activities that the model recommend
        return activ_list[0][0], round(activ_list[0][1]*100, 1) #リストの一番最初が結果の名前／類似度を小数点第一位まで出力

    def activ_fix(self, words, positive_words, negative_words):
        word_vec = self.get_wv(words)

        if positive_words == '' and negative_words == '': #両方とも空欄だったら
            activ_list = model.dv.most_similar(positive=word_vec) #list of activities that the model recommend
            return activ_list[0][0], round(activ_list[0][1]*100, 1) #リストの一番最初が結果の名前／類似度を小数点第一位まで出力

        elif negative_words=='': #negative_textだけが空欄だったら
            positive_vec = self.get_wv(positive_words)
            activ_list = model.dv.most_similar(positive=np.vstack([word_vec,positive_vec])) #numpy.vstack()で縦に結合
            return activ_list[0][0], round(activ_list[0][1]*100, 1)

        elif positive_words == '': #positive_textだけが空欄だったら
            negative_vec = self.get_wv(negative_words)
            activ_list = model.dv.most_similar(positive=word_vec, negative=negative_vec)
            return activ_list[0][0], round(activ_list[0][1]*100, 1)

        else: #どちらも入力されたら
            positive_vec = self.get_wv(positive_words)
            negative_vec = self.get_wv(negative_words)
            activ_list = model.dv.most_similar(positive=np.vstack([word_vec,positive_vec]), negative=negative_vec) #numpy.vstack()で縦に結合
            return activ_list[0][0], round(activ_list[0][1]*100, 1)


class Image:
    def __init__(self) -> None:
        pass

    def image(self, no):
        image = 'images/wordcloud.png'
        return image