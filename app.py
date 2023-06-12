# app.py

from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="task_manager"
)

# Create tasks table if it doesn't exist
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        completed BOOLEAN DEFAULT FALSE
    )
""")
cursor.close()

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    date = request.form['date']
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (name, date) VALUES (%s, %s)", (name, date))
    db.commit()
    cursor.close()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
