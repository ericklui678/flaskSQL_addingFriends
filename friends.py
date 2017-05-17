from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import md5
import os, binascii
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends') #database name
app.secret_key = 'ThisIsSecret'

@app.route('/')
def index():
    query = "SELECT name, age, DATE_FORMAT(created_at,'%M %d %Y') as friends_since FROM friends"
    # 'friends' holds a list of dictionaries from table info
    friends = mysql.query_db(query)
    return render_template('index.html', friends=friends)

@app.route('/create', methods=['POST'])
def process():
    # get form info
    name = request.form['name']
    age = request.form['age']

    # insert_query contains what query to run
    # :variables will contain values of that key
    insert_query = "INSERT INTO friends (name, age, created_at, updated_at) VALUES (:name, :age, NOW(), NOW())"

    query_data = {'name': name, 'age': age}

    # run the INSERT query with its data
    mysql.query_db(insert_query, query_data)

    return redirect('/')

app.run(debug = True)
