import sqlite3
import matplotlib.pyplot as plt

# Membuat koneksi ke database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Membuat tabel transaksi jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    amount REAL,
    type TEXT
)
''')

# Menambahkan fungsi untuk mencatat transaksi
def add_transaction(date, description, amount, type):
    cursor.execute('''
    INSERT INTO transactions (date, description, amount, type)
    VALUES (?, ?, ?, ?)
    ''', (date, description, amount, type))
    conn.commit()

# Contoh penggunaan fungsi
add_transaction('2025-02-25', 'Gaji Bulanan', 5000000, 'income')
add_transaction('2025-02-26', 'Belanja Bulanan', -1500000, 'expense')

# Menambahkan fungsi untuk menghasilkan laporan bulanan
def generate_monthly_report():
    cursor.execute('''
    SELECT strftime('%m-%Y', date) as month, 
           sum(case when type = 'income' then amount else 0 end) as total_income,
           sum(case when type = 'expense' then -amount else 0 end) as total_expense
    FROM transactions
    GROUP BY month
    ''')
    report = cursor.fetchall()
    for row in report:
        print(f"Bulan: {row[0]}, Pendapatan: {row[1]}, Pengeluaran: {row[2]}")

# Menghasilkan laporan bulanan
generate_monthly_report()

# Menutup koneksi database
conn.close()
