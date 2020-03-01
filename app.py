from flask import Flask, render_template,url_for,request,redirect
from sqlalchemy import create_engine
import pandas
import psycopg2


'''
参考にしたサイト
https://tanuhack.com/pandas-postgres-readto/

'''
connection_config = {
    'user': 'postgres',
    'password': '1racket1',
    'host': 'localhost',
    'port': '5432',
    'database': 'mydb'
}
connection = psycopg2.connect(**connection_config)

df = pandas.read_sql(sql='SELECT * FROM books;', con=connection) 
header = ['id','書籍名','著者','読了日','評価']
record = df.values.tolist() # DataFrameのインデックスを含まない全レコードの2次元配列のリスト

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',  header=header, record=record)

@app.route('/result', methods=['GET','POST'])
def addition():
    if request.method == "POST":
        book_id = len(record)+1
        res1 = request.form['書籍名']
        res2 = request.form['著者']
        res3 = request.form['読了日']
        res4 = request.form['評価']
        dict1={'id':[book_id],'name':[res1],'writer':[res2],'read_day':[res3],'rank':[res4]}
        engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))
        df = pandas.DataFrame(data=dict1)
        df.to_sql('books', con=engine, if_exists='append', index=False)
        return redirect(url_for('index'))

## おまじない
if __name__ == "__main__":
    app.run(debug=True)