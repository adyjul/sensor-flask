from flask import Flask, render_template, request
import sqlite3
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import pandas as pd

app = Flask(__name__)

train = pd.read_csv('F:\Tugas Kuliah\Piranti Cerdas\coba-tugas\Dataset.csv')
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
X_train = train.drop(columns=['Label'])
X_train = X_train.apply(le.fit_transform)


def getdata(query):
    # Connecting to sqlite
    conn = sqlite3.connect('data.db')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    sql = query
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows != None:
        label = rows[0][0]
    else:
        label = 'nodata'
    # Commit your changes in the database
    conn.commit()
    # Closing the connection
    conn.close()
    return label


@app.route('/')
def index():
    return render_template("http.html")


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        gx = request.form['gx']
        gy = request.form['gy']
        gz = request.form['gz']

        path = 'F:\Tugas Kuliah\Piranti Cerdas\coba-tugas\dtc.sav'
        model = pickle.load(open(path, 'rb'))
        result = model.predict([gx,gy,gz])
        result = le.inverse_transform([result])
        data = (gx, gy, gz, result)
        conn = sqlite3.connect('data.db')
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        sql = '''INSERT INTO data (gx,gy,gz,result) VALUES (?,?,?,?)'''
        cursor.execute(sql, data)
        # Commit your changes in the database
        conn.commit()
        # Closing the connection
        conn.close()
        return 'success'


@app.route('/reqlabel', methods=["GET", "POST"])
def reqlabel():
    if request.method == 'POST' and request.form['key'] == 'getdataLabel':
        query = '''SELECT result FROM data ORDER BY ID DESC LIMIT 1'''
        label = getdata(query)
        return label


@app.route('/reqx', methods=["GET", "POST"])
def reqx():
    if request.method == 'POST' and request.form['key'] == 'getdatax':
        query = '''SELECT gx FROM data ORDER BY ID DESC LIMIT 1'''
        label = getdata(query)
        return str(label)


@app.route('/reqy', methods=["GET", "POST"])
def reqy():
    if request.method == 'POST' and request.form['key'] == 'getdatay':
        query = '''SELECT gy FROM data ORDER BY ID DESC LIMIT 1'''
        label = getdata(query)
        return str(label)


@app.route('/reqz', methods=["GET", "POST"])
def reqz():
    if request.method == 'POST' and request.form['key'] == 'getdataz':
        query = '''SELECT gz FROM data ORDER BY ID DESC LIMIT 1'''
        label = getdata(query)
        return str(label)


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='127.0.0.1', port=80)