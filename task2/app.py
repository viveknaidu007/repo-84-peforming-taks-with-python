from flask import Flask, request, render_template
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Define root route for welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Define /addusers endpoint to handle POST and GET requests
@app.route('/addusers', methods=['POST', 'GET'])
def add_users():
    if request.method == 'POST':
        # Parse form input
        name = request.form.get('name')
        id = request.form.get('id')

        # Store data in SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, id INTEGER)")
        cursor.execute("INSERT INTO users (name, id) VALUES (?, ?)", (name, id))
        conn.commit()
        conn.close()

        # Query database for names with ids above 5
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE id > 5")
        result = cursor.fetchall()
        conn.close()

        # Extract names from result
        names_above_5 = [row[0] for row in result]

        # Render HTML template with result
        return render_template('adduser.html', names_above_5=names_above_5)

    elif request.method == 'GET':
        # If method is GET (initial page load), render HTML template without result
        return render_template('adduser.html')

if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True)
