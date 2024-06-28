import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import threading
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database/shop.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        contact_number = request.form['contact_number']
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        date_of_first_purchase = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notes = request.form['notes']

        conn = get_db_connection()
        conn.execute('INSERT INTO customers (contact_number, name, email, address, date_of_first_purchase, notes) VALUES (?, ?, ?, ?, ?, ?)',
                     (contact_number, name, email, address, date_of_first_purchase, notes))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('add_customer.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer_info():
    contact_number = request.args.get('contact_number')
    if contact_number is None:
        return "Customer contact number is required", 400

    conn = get_db_connection()
    
    if request.method == 'POST':
        total_price = request.form['total_price']
        amount_paid = request.form['amount_paid']
        remaining_amount = float(total_price) - float(amount_paid)
        notes = request.form['notes']
        date_of_transaction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn.execute('INSERT INTO transactions (customer_contact_number, date_of_transaction, total_price, amount_paid, remaining_amount, notes) VALUES (?, ?, ?, ?, ?, ?)',
                     (contact_number, date_of_transaction, total_price, amount_paid, remaining_amount, notes))
        conn.commit()
        conn.close()
        
        return redirect(url_for('customer_info', contact_number=contact_number))
    
    customer = conn.execute('SELECT * FROM customers WHERE contact_number = ?', (contact_number,)).fetchone()
    transactions = conn.execute('SELECT * FROM transactions WHERE customer_contact_number = ? ORDER BY date_of_transaction DESC', (contact_number,)).fetchall()
    conn.close()
    
    if customer is None:
        return f"No customer found with contact number {contact_number}", 404
    
    return render_template('customer_info.html', customer=customer, transactions=transactions)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jewelry Shop Ledger")
        self.setGeometry(100, 100, 1024, 768)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))
        self.setCentralWidget(self.browser)

def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
