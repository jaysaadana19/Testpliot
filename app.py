# app.py
from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)
conn = sqlite3.connect('urls.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, original_url TEXT, short_url TEXT)''')
conn.commit()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()
        c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_original(short_url):
    c.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    original_url = c.fetchone()
    if original_url:
        return redirect(original_url[0])
    return "URL not found"

if __name__ == '__main__':
    app.run(debug=True)
