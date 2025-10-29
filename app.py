from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = 1
    
    cursor.execute('SELECT * FROM todos WHERE user_id = %s', (user_id,))
    todos = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task and task.strip():
        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = 1
        
        cursor.execute('INSERT INTO todos (user_id, task) VALUES (%s, %s)', (user_id, task))
        conn.commit()
        conn.close()
        
        flash('Task added successfully!')
    else:
        flash('Task cannot be empty.')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE todos SET completed = TRUE WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    
    flash('Task marked as completed.')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM todos WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    
    flash('Task deleted successfully.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
