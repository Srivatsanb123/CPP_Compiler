from flask import Flask, render_template, request
import subprocess
import os
import time
import sqlite3


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    history = []
    code=request.form.get('cppcode')
    conn=sqlite3.connect('cppcodes.db')
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT)')
    sql_query = "INSERT INTO history (code) VALUES (?)"
    c.execute(sql_query, (code,))
    conn.commit()
    if request.method == 'POST':
        while not os.path.exists('cppcode.cpp'):
            time.sleep(0.1)
        try:
            subprocess.run(['g++', 'cppcode.cpp', '-o', 'cppcode'],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            output = error.stderr.decode('utf8')
            os.remove('cppcode.cpp')
            return render_template('index.html', output=output)
        inc = request.form.get('input')
        process = subprocess.Popen('./cppcode', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process.stdin.write(inc)
        out, err = process.communicate()
        output = out + err
        os.remove('cppcode.cpp')
        os.remove('cppcode.exe')
    c.execute('SELECT * FROM history WHERE code IS NOT NULL')
    rows = c.fetchall()
    for row in rows:
        history.append(row)
    conn.close()
    return render_template('index.html', output=output, history=history, cppcode=code)


@app.route('/history', methods=['GET', 'POST'])
def history():
    history = []
    conn=sqlite3.connect('cppcodes.db')
    c=conn.cursor()
    c.execute('SELECT * FROM history WHERE code IS NOT NULL')
    rows = c.fetchall()
    for row in rows:
        history.append(row)
    conn.close()
    return render_template('history.html',history=history)

if __name__ == '__main__':
    app.run(debug=True)