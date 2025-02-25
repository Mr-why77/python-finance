from app import app
from flask import render_template, request, redirect, url_for
import sqlite3

# Fungsi untuk membuat koneksi ke database
def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route untuk halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

# Route untuk menambahkan transaksi baru
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        type = request.form['type']

        conn = get_db_connection()
        conn.execute('INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)',
                     (date, description, amount, type))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add.html')

# Route untuk mengedit transaksi
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    transaction = conn.execute('SELECT * FROM transactions WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = request.form['amount']
        type = request.form['type']

        conn.execute('UPDATE transactions SET date = ?, description = ?, amount = ?, type = ? WHERE id = ?',
                     (date, description, amount, type, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', transaction=transaction)

# Route untuk menghapus transaksi
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
