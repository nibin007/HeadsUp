import pickle
import preprocess_kgptalkie as ps
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pandas as pd
import numpy as np
from .models import Profile, Post, LikePost, FollowersCount,Likedby,Comment,DiaryModel,ReportModel,Suicidal

file = open("D:\socialmediaapp\core\suicidal.pkl","rb")
clff = pickle.load(file)
file.close()

#df=pd.read_csv('twitter-suicidal_data.csv')  

def get_clean(x):
    x = str(x).lower().replace('\\', '').replace('_', ' ')
    x = ps.cont_exp(x)
    x = ps.remove_emails(x)
    x = ps.remove_urls(x)
    x = ps.remove_html_tags(x)
    x = ps.remove_rt(x)
    x = ps.remove_accented_chars(x)
    x = ps.remove_special_chars(x)
    x = re.sub("(.)\\1{2,}", "\\1", x)
    return x
#df['tweet']=df['tweet'].apply(lambda x:get_clean(x))
#df.to_pickle("preprocessed_data.pkl")
def preds(x,objs):
    caption=x
    print("hiiiii")
    df = pd.read_pickle("D:\socialmediaapp\core\preprocessed_data.pkl")
    tweet_series = df['tweet']
    tfidt=TfidfVectorizer(max_features=20000,ngram_range=( 1,3),analyzer='char')
    X=tfidt.fit_transform(tweet_series)
    x=get_clean(x)
    vec=tfidt.transform([x])
    a=clff.predict(vec)[0]
    if a==1:
        print("hey!")
        existing_suicidal = Suicidal.objects.filter(user=objs)
        if existing_suicidal.exists():
             existing_suicidal.delete()
        saves=Suicidal.objects.create(user=objs,caption=caption)  
        saves.save()
        