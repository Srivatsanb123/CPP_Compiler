from flask import Flask, render_template, request
import subprocess
import os
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        code=request.form.get('cppcode')
        with open('cppcode.cpp','w') as f:
            f.write(code)
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
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
