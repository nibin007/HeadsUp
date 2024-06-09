import os
import pandas as pd
import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.layers import TextVectorization

df = pd.read_csv(r'D:\socialmediaapp\core\train.csv')
X = df['comment_text']
y = df[df.columns[2:]].values
MAX_FEATURES = 200000 
vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=180,
                               output_mode='int')
vectorizer.adapt(X.values)

model = tf.keras.models.load_model(r'D:\socialmediaapp\core\toxic6epoch.h5')
#input_str = vectorizer('You look beautiful')
#res = model.predict(np.expand_dims(input_str,0))
#print(res)
#file = open("modeltox7epoch.pkl","rb")
#model2 = pickle.load(file)
#file.close()
# def score_comment(comment):
#     print('helo')
#     vectorized_comment = vectorizer(comment)
#     results = model.predict(np.expand_dims(vectorized_comment,0))
#     print(results)
#     text = ''
#     for idx, col in enumerate(df.columns[2:]):
#         text += '{}: {}\n'.format(col, results[0][idx]>0.5)

#     return text

def analyze_comment(comment_scores):
    print(comment_scores.values())
    if all(value is False for value in comment_scores.values()):
        print('good')
        print("hello bro")
        return 'good'
    else:
        true_categories = [key for key, value in comment_scores.items() if value is True]
        #print(true_categories)
        print(', '.join(true_categories))
        return ', '.join(true_categories)
    
def score_comment2(comment):
    vectorized_comment = vectorizer(comment)
    results = model.predict(np.expand_dims(vectorized_comment, 0))
    scores_dict = {}
    for idx, col in enumerate(df.columns[2:]):
        scores_dict[col] = results[0][idx] > 0.5  
    a = {key: bool(value) for key, value in scores_dict.items()}  
    if all(value is False for value in a.values()):
        print('good')
        print("hello bro")
        return 'good'
    else:
        true_categories = [key for key, value in a.items() if value is True]
        #print(true_categories)
        print(', '.join(true_categories))
        return ', '.join(true_categories)    

#score_comment2('nice one bro')
#a = {key: bool(value) for key, value in a.items()}
#a = {key: value == 'True' for key, value in a.items()}

#finals=analyze_comment(a)


