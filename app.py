from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# Database initialization
def init_db():
    conn = sqlite3.connect('budget_tracker.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    
    # Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    
    # Budgets table
    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    period TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    
    # Groups table
    c.execute('''CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_by INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )''')
    
    # Group members table
    c.execute('''CREATE TABLE IF NOT EXISTS group_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES groups (id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(group_id, user_id)
                )''')
    
    # Group expenses table
    c.execute('''CREATE TABLE IF NOT EXISTS group_expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    paid_by INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date DATE NOT NULL,
                    split_type TEXT DEFAULT 'equal',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES groups (id),
                    FOREIGN KEY (paid_by) REFERENCES users (id)
                )''')
    
    # Expense splits table
    c.execute('''CREATE TABLE IF NOT EXISTS expense_splits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expense_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    settled BOOLEAN DEFAULT FALSE,
                    settled_at TIMESTAMP,
                    FOREIGN KEY (expense_id) REFERENCES group_expenses (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect('budget_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash('Email already registered', 'error')
            conn.close()
            return render_template('login.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                    (name, email, password_hash))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get recent transactions
    recent_transactions = conn.execute('''
        SELECT * FROM transactions 
        WHERE user_id = ? 
        ORDER BY date DESC, created_at DESC 
        LIMIT 10
    ''', (session['user_id'],)).fetchall()
    
    # Get total income and expenses for current month
    current_month = datetime.now().strftime('%Y-%m')
    monthly_income = conn.execute('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE user_id = ? AND type = 'income' AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%')).fetchone()['total']
    
    monthly_expenses = conn.execute('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE user_id = ? AND type = 'expense' AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%')).fetchone()['total']
    
    # Get budget data
    budgets = conn.execute('''
        SELECT * FROM budgets WHERE user_id = ?
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_transactions=recent_transactions,
                         monthly_income=monthly_income,
                         monthly_expenses=monthly_expenses,
                         budgets=budgets)

@app.route('/transactions')
def transactions():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT * FROM transactions 
        WHERE user_id = ? 
        ORDER BY date DESC, created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('transaction_management.html', transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    transaction_type = request.form['type']
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form.get('description', '')
    date = request.form['date']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO transactions (user_id, type, category, amount, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], transaction_type, category, amount, description, date))
    conn.commit()
    conn.close()
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('transactions'))

@app.route('/budgets')
def budgets():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    budgets = conn.execute('''
        SELECT * FROM budgets WHERE user_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('budget_management.html', budgets=budgets)

@app.route('/add_budget', methods=['POST'])
def add_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    category = request.form['category']
    amount = float(request.form['amount'])
    period = request.form['period']
    
    conn = get_db_connection()
    # Check if budget already exists for this category
    existing_budget = conn.execute('''
        SELECT * FROM budgets WHERE user_id = ? AND category = ?
    ''', (session['user_id'], category)).fetchone()
    
    if existing_budget:
        # Update existing budget
        conn.execute('''
            UPDATE budgets SET amount = ?, period = ? 
            WHERE user_id = ? AND category = ?
        ''', (amount, period, session['user_id'], category))
    else:
        # Create new budget
        conn.execute('''
            INSERT INTO budgets (user_id, category, amount, period)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], category, amount, period))
    
    conn.commit()
    conn.close()
    
    flash('Budget updated successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/group_expenses')
def group_expenses():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get user's groups
    user_groups = conn.execute('''
        SELECT g.*, u.name as created_by_name,
               COUNT(gm.user_id) as member_count
        FROM groups g
        JOIN users u ON g.created_by = u.id
        JOIN group_members gm ON g.id = gm.group_id
        WHERE g.id IN (
            SELECT group_id FROM group_members WHERE user_id = ?
        )
        GROUP BY g.id
        ORDER BY g.created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    # Get recent group expenses
    recent_expenses = conn.execute('''
        SELECT ge.*, g.name as group_name, u.name as paid_by_name,
               es.amount as user_owes
        FROM group_expenses ge
        JOIN groups g ON ge.group_id = g.id
        JOIN users u ON ge.paid_by = u.id
        LEFT JOIN expense_splits es ON ge.id = es.expense_id AND es.user_id = ?
        WHERE g.id IN (
            SELECT group_id FROM group_members WHERE user_id = ?
        )
        ORDER BY ge.created_at DESC
        LIMIT 10
    ''', (session['user_id'], session['user_id'])).fetchall()
    
    # Get balance summary (what user owes/is owed)
    balance_summary = conn.execute('''
        SELECT 
            SUM(CASE WHEN ge.paid_by = ? THEN es.amount ELSE 0 END) as total_owed_to_user,
            SUM(CASE WHEN ge.paid_by != ? AND es.settled = 0 THEN es.amount ELSE 0 END) as total_user_owes
        FROM group_expenses ge
        JOIN expense_splits es ON ge.id = es.expense_id
        WHERE es.user_id = ?
    ''', (session['user_id'], session['user_id'], session['user_id'])).fetchone()
    
    conn.close()
    
    return render_template('group_expenses.html', 
                         user_groups=user_groups,
                         recent_expenses=recent_expenses,
                         balance_summary=balance_summary)

@app.route('/create_group', methods=['POST'])
def create_group():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    name = request.form['name']
    description = request.form.get('description', '')
    
    conn = get_db_connection()
    
    # Create group
    cursor = conn.execute('''
        INSERT INTO groups (name, description, created_by)
        VALUES (?, ?, ?)
    ''', (name, description, session['user_id']))
    
    group_id = cursor.lastrowid
    
    # Add creator as first member
    conn.execute('''
        INSERT INTO group_members (group_id, user_id)
        VALUES (?, ?)
    ''', (group_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    flash('Group created successfully!', 'success')
    return redirect(url_for('group_expenses'))

@app.route('/join_group', methods=['POST'])
def join_group():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    group_id = request.form['group_id']
    
    conn = get_db_connection()
    
    # Check if group exists
    group = conn.execute('SELECT * FROM groups WHERE id = ?', (group_id,)).fetchone()
    if not group:
        flash('Group not found!', 'error')
        conn.close()
        return redirect(url_for('group_expenses'))
    
    # Check if already a member
    existing_member = conn.execute('''
        SELECT * FROM group_members WHERE group_id = ? AND user_id = ?
    ''', (group_id, session['user_id'])).fetchone()
    
    if existing_member:
        flash('You are already a member of this group!', 'error')
    else:
        # Add user to group
        conn.execute('''
            INSERT INTO group_members (group_id, user_id)
            VALUES (?, ?)
        ''', (group_id, session['user_id']))
        conn.commit()
        flash('Successfully joined the group!', 'success')
    
    conn.close()
    return redirect(url_for('group_expenses'))

@app.route('/add_group_expense', methods=['POST'])
def add_group_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    group_id = request.form['group_id']
    description = request.form['description']
    amount = float(request.form['amount'])
    date = request.form['date']
    split_type = request.form.get('split_type', 'equal')
    
    conn = get_db_connection()
    
    # Get group members
    members = conn.execute('''
        SELECT user_id FROM group_members WHERE group_id = ?
    ''', (group_id,)).fetchall()
    
    if not members:
        flash('No members found in this group!', 'error')
        conn.close()
        return redirect(url_for('group_expenses'))
    
    # Create expense
    cursor = conn.execute('''
        INSERT INTO group_expenses (group_id, paid_by, description, amount, date, split_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (group_id, session['user_id'], description, amount, date, split_type))
    
    expense_id = cursor.lastrowid
    
    # Split expense equally among members
    split_amount = amount / len(members)
    
    for member in members:
        conn.execute('''
            INSERT INTO expense_splits (expense_id, user_id, amount)
            VALUES (?, ?, ?)
        ''', (expense_id, member['user_id'], split_amount))
    
    conn.commit()
    conn.close()
    
    flash('Group expense added successfully!', 'success')
    return redirect(url_for('group_expenses'))

@app.route('/settle_expense/<int:expense_id>')
def settle_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Mark user's split as settled
    conn.execute('''
        UPDATE expense_splits 
        SET settled = 1, settled_at = CURRENT_TIMESTAMP
        WHERE expense_id = ? AND user_id = ?
    ''', (expense_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    flash('Expense settled successfully!', 'success')
    return redirect(url_for('group_expenses'))

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get monthly data for charts
    monthly_data = conn.execute('''
        SELECT 
            strftime('%Y-%m', date) as month,
            type,
            SUM(amount) as total
        FROM transactions 
        WHERE user_id = ?
        GROUP BY month, type
        ORDER BY month DESC
        LIMIT 12
    ''', (session['user_id'],)).fetchall()
    
    # Get category breakdown
    category_data = conn.execute('''
        SELECT 
            category,
            SUM(amount) as total
        FROM transactions 
        WHERE user_id = ? AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('reports_and_analytics.html', 
                         monthly_data=monthly_data,
                         category_data=category_data)

# API endpoints for AJAX requests
@app.route('/api/transactions')
def api_transactions():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT * FROM transactions 
        WHERE user_id = ? 
        ORDER BY date DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify([dict(transaction) for transaction in transactions])

@app.route('/api/dashboard_data')
def api_dashboard_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    
    # Get current month data
    current_month = datetime.now().strftime('%Y-%m')
    
    income = conn.execute('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE user_id = ? AND type = 'income' AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%')).fetchone()['total']
    
    expenses = conn.execute('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE user_id = ? AND type = 'expense' AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%')).fetchone()['total']
    
    conn.close()
    
    return jsonify({
        'income': income,
        'expenses': expenses,
        'balance': income - expenses
    })

if __name__ == '__main__':
    app.run(debug=True)
