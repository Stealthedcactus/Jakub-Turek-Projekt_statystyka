import numpy as np
from flask import Flask, request, render_template
from flask_restful import Resource, Api
import sqlite3
import pickle


def string_into_number(string): return int(string == 'm')
def is_last_a(string): return int(string[-1] == 'a')
def name_length(string): return int(len(string))

def predict(string_):
    string = string_.lower()
    temp = np.array([[name_length(string), is_last_a(string)]])
    return model.predict(temp)

def list_to_dict(input_list, cols):
    lista = []
    for i in range(len(input_list)):
        dictionary = {}
        for x in range(len(cols)):
            dictionary[cols[x]] = input_list[i][x]
        lista.append(dictionary)
    return lista

def column_list(cursor):
    columns = []
    for i in range(len(cursor.description)):
        columns.append(cursor.description[i][0])
    return columns

pkl_filename = "model_trained.pkl"

with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)


app = Flask(__name__)
api = Api(app)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/rm')
def rm():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""DELETE FROM zapytania""")
    conn.commit()
    conn.close()
    return render_template('SPRAWDZANIE.html', title='Home')


@app.route('/', methods=['GET', 'POST'])
def sprawdzanie():
    if request.method == 'POST':
        uploaded_name = request.form['INPUT_FROM_USER']
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        if (' ' in uploaded_name ):
            return render_template('SPRAWDZANIE.html', title='Home')

        if predict(uploaded_name) == 0:
            c.execute("""INSERT INTO zapytania (imie, plec) VALUES (?,?)""", [uploaded_name, 'kobieta'])
            conn.commit()
            conn.close()
            return render_template('SPRAWDZANIE.html', title='Home', user=uploaded_name, gender='kobieta')

        if predict(uploaded_name) == 1:
            c.execute("""INSERT INTO zapytania (imie, plec) VALUES (?,?)""", [uploaded_name, 'mezczyzna'])
            conn.commit()
            conn.close()
            return render_template('SPRAWDZANIE.html', title='Home', user=uploaded_name, gender='mężczyzna')

    return render_template('SPRAWDZANIE.html', title='Home')

@app.route('/baza', methods=['GET'])
def baza():
    c = sqlite3.connect("database.db").cursor()
    c.execute("""SELECT * FROM zapytania""")
    temp = c.fetchall()
    logi = list_to_dict(temp, column_list(c))
    c.close()
    return render_template('baza.html', logi=logi)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.run(host='0.0.0.0', port=5000)
