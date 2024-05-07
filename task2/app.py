import json
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, id INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/adduser', methods=['POST'])
def add_user():
    init_db()
    data = request.get_json()
    name = data['name']
    id = data['id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, id) VALUES (?, ?)", (name, id))
    conn.commit()
    conn.close()
    result = {"names_with_ids_above_5": []}
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM users WHERE id > 5")
    rows = c.fetchall()
    for row in rows:
        result["names_with_ids_above_5"].append(row[0])
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)