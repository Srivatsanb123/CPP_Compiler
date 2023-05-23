from flask import Flask, render_template, request
import subprocess
import os
import sqlite3
import datetime


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    history = []
    code=request.form.get('cppcode')
    date,time=str(datetime.datetime.now()).split()
    time=time[:8]
    conn=sqlite3.connect('cppcodes.db')
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history (code TEXT,output TEXT,date TEXT,time TEXT)')
    conn.commit()
    if request.method == 'POST':
        with open('cppcode.cpp', 'w') as f:
            for line in code.splitlines():
                f.write(line + '\n')
        try:
            subprocess.run(['g++', 'cppcode.cpp', '-o', 'cppcode'],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            output = error.stderr.decode('utf8')
            os.remove('cppcode.cpp')
            c.execute('INSERT INTO history(code,output,date,time) VALUES (?,?,?,?)', (code,output,date,time))
            conn.commit()
            c.execute('SELECT code,output FROM history WHERE code IS NOT NULL')
            rows = c.fetchall()
            for row in rows:
                history.append(row)
            conn.close()
            return render_template('index.html', output=output,history=history,cppcode=code)
        inc = request.form.get('input')
        process = subprocess.Popen('./cppcode', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process.stdin.write(inc)
        out, err = process.communicate()
        output = out + err
        os.remove('cppcode.cpp')
        os.remove('cppcode.exe')
    c.execute('INSERT INTO history(code,output,date,time) VALUES (?,?,?,?)', (code,output,date,time))
    conn.commit()
    c.execute('SELECT code,output FROM history WHERE code IS NOT NULL')
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