# Personal Budget Tracker - Flask Application

## Overview
This is a Flask-based personal budget tracking application converted from the original HTML version. It includes user authentication, transaction management, budget tracking, and financial reporting features.

## Features
- ✅ User Registration & Login
- ✅ Dashboard with financial overview
- ✅ Transaction Management (Add, View, Track)
- ✅ Budget Management (Set limits by category)
- ✅ Reports & Analytics with Charts
- ✅ Group Expenses (Create groups, split bills, track settlements)
- ✅ SQLite Database for data persistence
- ✅ Session-based authentication
- ✅ Responsive design with Tailwind CSS

## Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. First Time Setup
1. Navigate to `http://localhost:5000`
2. You'll be redirected to the login page
3. Create a new account using the registration form
4. Start adding transactions and setting budgets!

## Database
The application uses SQLite database (`budget_tracker.db`) which will be created automatically when you first run the app. The database includes:
- Users table (for authentication)
- Transactions table (income/expense records)
- Budgets table (spending limits by category)
- Groups table (expense sharing groups)
- Group_members table (group membership)
- Group_expenses table (shared expenses)
- Expense_splits table (individual shares and settlements)

## File Structure
```
personal_budget_tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── budget_tracker.db     # SQLite database Created 
├── templates/            
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── transaction_management.html
│   ├── budget_management.html
│   ├── group_expenses.html
│   └── reports_and_analytics.html
└── static/              # CSS, JS, and other static files
    └── css/
        ├── main.css
        └── tailwind.css
```

## Usage

### Adding Transactions
1. Go to Dashboard or Transactions page
2. Fill in the transaction form with:
   - Type (Income/Expense)
   - Category
   - Amount
   - Date
   - Description (optional)
3. Click "Add Transaction"

### Setting Budgets
1. Navigate to Budget Management
2. Enter category name, budget amount, and period (monthly/weekly/yearly)
3. Click "Set Budget"

### Viewing Reports
1. Go to Reports & Analytics page
2. View charts showing:
   - Monthly income vs expenses
   - Category breakdown
   - Spending trends

### Using Group Expenses
1. **Create a Group:**
   - Navigate to Group Expenses page
   - Fill in group name and description
   - Click "Create Group" - you'll get a Group ID
2. **Invite Others:**
   - Share the Group ID with friends/family
   - They can join using "Join Existing Group"
3. **Add Shared Expenses:**
   - Select a group and add expense details
   - Amount is automatically split equally among members
4. **Settle Up:**
   - View who owes what in the expenses table
   - Click "Settle Up" to mark your portion as paid

## Security Notes
- Change the `app.secret_key` in `app.py` before deploying to production
- The current setup is for development only
- For production, use a proper database like PostgreSQL
- Implement proper password policies and security measures

## Troubleshooting
- If you get import errors, make sure all dependencies are installed: `pip install -r requirements.txt`
- If the database doesn't work, delete `budget_tracker.db` and restart the app
- For port conflicts, change the port in `app.run(debug=True, port=5001)`

## Demo Credentials
You can create your own account or use these demo credentials:
- Email: demo@example.com
- Password: password123

Enjoy tracking your finances! 
