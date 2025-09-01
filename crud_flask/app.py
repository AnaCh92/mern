from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from config import Config
from database import init_app, get_db
from models import User

app = Flask(__name__)
app.secret_key = '1234'  # Cambia esto por una clave segura

# Inicializar la base de datos
init_app(app)

# Crear la tabla si no existe
with app.app_context():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

@app.route('/')
def index():
    users = User.get_all()
    return render_template('index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        if User.create(name, email, phone):
            flash('Usuario creado exitosamente!', 'success')
            return redirect(url_for('index'))
        else:
            flash('El email ya existe!', 'error')
    
    return render_template('create.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        flash('Usuario no encontrado!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        User.update(user_id, name, email, phone)
        flash('Usuario actualizado exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', user=user)

@app.route('/view/<int:user_id>')
def view(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        flash('Usuario no encontrado!', 'error')
        return redirect(url_for('index'))
    
    return render_template('view.html', user=user)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        flash('Usuario no encontrado!', 'error')
    else:
        User.delete(user_id)
        flash('Usuario eliminado exitosamente!', 'success')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

#databse.py
def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split('/')[0].split(':')[0],
        database=app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1],
        user=app.config['SQLALCHEMY_DATABASE_URI'].split('://')[1].split(':')[0],
        password=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[2].split('@')[0],
        port=app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split('/')[0].split(':')[1]
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios;')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)