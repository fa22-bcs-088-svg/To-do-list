from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

def get_db_connection():
    # Retry for up to ~30 seconds (MySQL can be slow to initialize)
    for i in range(30):
        try:
            conn = mysql.connector.connect(
                host='db',         
                user='root',
                password='root',
                database='todos_db'
            )
            print("✅ Connected to MySQL!")
            return conn
        except mysql.connector.Error as e:
            print(f"⏳ MySQL not ready yet ({e}), retrying {i+1}/30...")
            time.sleep(2)
    raise Exception("❌ Could not connect to MySQL after multiple attempts.")


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            task TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM todos ORDER BY id DESC')
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    name = request.form.get('name')
    task = request.form.get('task')
    if name and task:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (name, task) VALUES (%s, %s)', (name, task))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5020, debug=True)
