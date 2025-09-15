# Personal Budget Tracker

A full-stack financial management tool designed to help users track income, expenses, and budgets with a clean, responsive interface. Built with Node.js, Express, MongoDB, and a modern frontend using Tailwind CSS and Chart.js.

 <!-- TODO: Replace with a real screenshot of your app! -->

---

## 🚀 Features

-   📊 **Dashboard & Visualization**: Get an instant overview of your finances with summary cards and interactive charts (Pie chart for category spending, Bar chart for income vs. expense).
-   💸 **Transaction Management**: Full CRUD (Create, Read, Update, Delete) functionality for income and expense entries.
-   🎯 **Category-Based Budgeting**: Set monthly spending limits for different categories (e.g., Food, Transport) and track your progress in real-time.
-   📱 **Responsive Design**: A mobile-first design built with Tailwind CSS ensures a seamless experience on any device.
-   🔍 **Search & Filtering**: Easily find transactions by date, type, or category.
-   👥 **Group Expense Management (Coming Soon)**: Future support for creating groups, splitting bills, and tracking shared balances.

---

## 🛠️ Tech Stack

-   **Backend**: Node.js, Express.js
-   **Database**: MongoDB with Mongoose
-   **Frontend**: HTML5, Vanilla JavaScript (DOM Manipulation)
-   **Styling**: Tailwind CSS
-   **Data Visualization**: Chart.js

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
-   [Node.js](https://nodejs.org/) (v14.x or higher)
-   [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
-   [MongoDB](https://www.mongodb.com/try/download/community) installed locally or a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account.

---

## ⚙️ Installation & Setup

Follow these steps to get your development environment running.

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/personal-budget-tracker.git
cd personal-budget-tracker
```
2. Backend Setup
The backend serves the API that the frontend communicates with.
```bash
# Navigate to the backend directory
cd backend
# Install dependencies
npm install

# Create a .env file in the /backend directory
# (copy from .env.example)
cp .env.example .env
Now, open the newly created .env file and add your MongoDB connection string and a port number:
code
Env
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/budget-tracker?retryWrites=true&w=majority
PORT=3000
```
**3. Frontend Setup**
The frontend contains all the HTML, CSS, and client-side JavaScript.
```bash
# Navigate to the frontend directory from the root
cd frontend

# Install dev dependencies (for Tailwind CSS)
npm install
```
**4. Start the Servers**
You'll need two separate terminals to run both the backend and frontend development servers.
Terminal 1: Start the Backend Server
```bash
# In the /backend directory
npm run dev
```
Your Node.js API should now be running on http://localhost:3000.
Terminal 2: Start the Frontend Tailwind Compiler
```bash
# In the /frontend directory
npm run dev
```
#This command will watch for changes in your HTML and tailwind.css files and automatically recompile your main.css file. To view the app, open frontend/index.html in your browser, preferably with a live-reloading extension like Live Server for VS Code.
---
## 📁 Project Structure
The project is organized into two main parts: backend and frontend.
```bash
personal-budget-tracker/
├── backend/
│   ├── models/           # Mongoose schemas (Transaction, Budget)
│   ├── routes/           # API routes (transactions.js, budgets.js)
│   ├── .env              # Environment variables (secret)
│   ├── .env.example      # Example environment variables
│   ├── package.json
│   └── server.js         # Main Express server entry point
│
├── frontend/
│   ├── css/
│   │   ├── tailwind.css  # Tailwind source file with custom utilities
│   │   └── main.css      # Compiled CSS (generated)
│   ├── js/
│   │   └── main.js       # All client-side DOM manipulation & API calls
│   ├── index.html        # Main dashboard page
│   ├── budgets.html      # Budget management page
│   ├── package.json      # Dev dependencies for Tailwind
│   └── tailwind.config.js# Tailwind CSS configuration
│
└── README.md
```
---
## 🎨 Styling & Customization
This project uses Tailwind CSS for styling.
Source File: All custom styles and Tailwind directives are in frontend/css/tailwind.css.
Configuration: To customize colors, fonts, or extend Tailwind's default theme, edit the frontend/tailwind.config.js file.
Build Command: The npm run dev script in the frontend directory uses the Tailwind CLI in "watch" mode for development.
Build for Production
To generate a minified and purged CSS file for production, run the following command in the frontend directory:
```bash
npm run build:css
```
---
## 📱 Responsive Design
#The app is built with a responsive, mobile-first approach using Tailwind CSS's standard breakpoints:
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
---
##🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
