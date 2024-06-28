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
        name = request.form['name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        date_of_first_purchase = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notes = request.form['notes']

        conn = get_db_connection()
        conn.execute('INSERT INTO customers (name, contact_number, email, address, date_of_first_purchase, notes) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, contact_number, email, address, date_of_first_purchase, notes))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('add_customer.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer_info():
    id = request.args.get('id', type=int)
    if id is None:
        return "Customer ID is required", 400

    conn = get_db_connection()
    
    if request.method == 'POST':
        total_price = request.form['total_price']
        amount_paid = request.form['amount_paid']
        remaining_amount = float(total_price) - float(amount_paid)
        notes = request.form['notes']
        date_of_transaction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn.execute('INSERT INTO transactions (customer_id, date_of_transaction, total_price, amount_paid, remaining_amount, notes) VALUES (?, ?, ?, ?, ?, ?)',
                     (id, date_of_transaction, total_price, amount_paid, remaining_amount, notes))
        conn.commit()
        conn.close()
        
        return redirect(url_for('customer_info', id=id))
    
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()
    transactions = conn.execute('SELECT * FROM transactions WHERE customer_id = ? ORDER BY date_of_transaction DESC', (id,)).fetchall()
    conn.close()
    
    if customer is None:
        return f"No customer found with ID {id}", 404
    
    return render_template('customer_info.html', customer=customer, transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        date_of_first_purchase = datetime.now().strftime("%Y-%m-%d")
        notes = request.form['notes']
        conn = get_db_connection()
        conn.execute('INSERT INTO customers (name, contact_number, email, address, date_of_first_purchase, notes) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, contact_number, email, address, date_of_first_purchase, notes))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_customer.html')

if __name__ == '__main__':
    app.run(debug=True)
