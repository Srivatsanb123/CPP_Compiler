from flask import Flask, render_template, request,session,redirect
import subprocess
import os
import sqlite3
import datetime

conn=sqlite3.connect('users.db')
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Profiles (name VARCHAR(20), email VARCHAR(50), password VARCHAR(20))')
conn.commit()
c.close()

app = Flask(__name__)

app.secret_key = '1234'

@app.route('/login', methods=['GET','POST'])
def login():
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        c.execute("SELECT * FROM Profiles WHERE email=? AND password=?",(email,password))
        data=c.fetchone()
        c.close()
        if data:
            session['username']=data[0]
            return redirect('/')
        else:
            err='Invalid credentials. Please try again.'
            return render_template('login.html',error=err)
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        email=request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']
        if pwd==cpwd:
            c.execute("SELECT * FROM Profiles WHERE email=?",(email,))
            data=c.fetchall()
            if not data:
                c.execute("INSERT INTO Profiles VALUES(?,?,?)",(username,email,cpwd))
                conn.commit()
                session['username']=username
                query='CREATE TABLE IF NOT EXISTS '+session['username']+'(code TEXT,output TEXT,date TEXT,time TEXT)'
                c.execute(query)
                conn.commit()
                return redirect('/')
            else:
                err='User already exists'
                return render_template('signup.html',error=err)
        else:
            err='Pasword did not match'
            return render_template('signup.html',error=err)
    else:
        return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect('/login')
    output = ''
    history = []
    code=request.form.get('cppcode')
    date,time=str(datetime.datetime.now()).split()
    time=time[:8]
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    file=session['username']+'.cpp'
    obj=session['username']+'.exe'
    if request.method == 'POST':
        with open(file, 'w') as f:
            for line in code.splitlines():
                f.write(line + '\n')
        try:
            subprocess.run(['g++', file, '-o', obj],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            output = error.stderr.decode('utf8')
            os.remove(file)
            c.execute('INSERT INTO '+session['username']+'(code,output,date,time) VALUES (?,?,?,?)', (code,output,date,time))
            conn.commit()
            c.execute('SELECT code,output FROM '+session['username']+' WHERE code IS NOT NULL')
            rows = c.fetchall()
            for row in rows:
                history.append(row)
            conn.close()
            return render_template('index.html',username=session['username'], output=output,history=history,cppcode=code)
        inc = request.form.get('input')
        process = subprocess.Popen('./'+obj, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process.stdin.write(inc)
        out, err = process.communicate()
        output = out + err
        os.remove(file)
        os.remove(obj)
    c.execute('INSERT INTO '+session['username']+'(code,output,date,time) VALUES (?,?,?,?)', (code,output,date,time))
    conn.commit()
    c.execute('SELECT code,output FROM '+session['username']+' WHERE code IS NOT NULL')
    rows = c.fetchall()
    for row in rows:
        history.append(row)
    conn.close()
    return render_template('index.html',username=session['username'], output=output, history=history, cppcode=code)

@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'username' not in session:
        return redirect('/login')
    history = []
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    c.execute('SELECT * FROM '+session['username']+' WHERE code IS NOT NULL')
    rows = c.fetchall()
    for row in rows:
        history.append(row)
    conn.close()
    return render_template('history.html',history=history)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/clear')
def clear():
    if 'username' not in session:
        return redirect('/login')
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    c.execute('DELETE FROM '+session['username'])
    conn.commit()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
