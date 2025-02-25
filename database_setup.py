import sqlite3
import matplotlib.pyplot as plt


conn = sqlite3.connect('finance.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    amount REAL,
    type TEXT
)
''')


def add_transaction(date, description, amount, type):
    cursor.execute('''
    INSERT INTO transactions (date, description, amount, type)
    VALUES (?, ?, ?, ?)
    ''', (date, description, amount, type))
    conn.commit()


add_transaction('2025-02-25', 'Gaji Bulanan', 5000000, 'income')
add_transaction('2025-02-26', 'Belanja Bulanan', -1500000, 'expense')


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


generate_monthly_report()


conn.close()
