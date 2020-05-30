import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from flask import Flask, request, render_template
from flask_restful import Resource, Api
import sqlite3
import pickle

df = pd.read_csv("https://sebkaz.github.io/teaching/PrzetwarzanieDanych/data/polish_names.csv")
def string_into_number(string): return int(string == 'm')
def is_last_a(string): return int(string[-1] == 'a')
def name_length(string): return int(len(string))

df['target'] = df['gender'].map(string_into_number)
df['len_name'] = df['name'].map(name_length)
df['is_last_a'] = df['name'].map(is_last_a)

y = df['target'].values
X = df[['len_name', 'is_last_a']].values

model = DecisionTreeClassifier()
model.fit(X, y)

y_pred_lr = model.predict(X)
accuracy_score(y, y_pred_lr)

dd = np.array([[name_length("Agata"), is_last_a("Agata")]])
test_prediction = model.predict(dd)

pkl_filename = "model_trained.pkl"

with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)