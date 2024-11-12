from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import DATABASE_CONFIG

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  

def get_db_connection():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO radcheck (username, attribute, op, value) VALUES (%s, 'Cleartext-Password', ':=', %s)",
                (email, senha)
            )
            conn.commit()
            flash('Registrado com sucesso! Faça o login.', 'success') 
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Erro: {err}', 'danger')  
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM radcheck WHERE username = %s AND attribute = 'Cleartext-Password' AND value = %s",
            (email, senha)
        )
        user = cursor.fetchone()
        
        if user:
            flash('Login bem-sucedido!', 'success') 
            return redirect(url_for('dashboard'))
        else:
            flash('Acesso negado!', 'danger') 

            cursor.close()
        conn.close()
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Bem-vindo ao portal!"

if __name__ == '__main__':
    app.run(debug=True)