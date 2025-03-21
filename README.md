# 🛒 Flask E-Commerce Web Application with Web-Application-Firewall 

This is a basic Flask e-commerce web application with user authentication, product listing, and a cart system. The `app.py` application is intentionally vulnerable to SQL Injection, XSS Payloads, Javascript Payloads, etc to demonstrate common web application security risks. `appwaf.py` is protected with a Web-Application-Firewall to prevent attack above mentioned. 

---

## 📚 Table of Contents
- [Project Description](#-project-description)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [How to Perform SQL Injection](#-how-to-perform-sql-injection)
- [Security Recommendations](#-security-recommendations)

---

## 📄 Project Description
This web application allows users to:
- Register and log in.
- Browse a list of products.
- Add products to the cart and view the cart.
- Checkout and clear the cart.

⚠️ **Note:** This version is intentionally vulnerable to SQL injection attacks to showcase how attackers can manipulate the SQL queries.

---

## 🚀 Features
- User Registration & Login
- Product Listing
- Add to Cart / View Cart
- Checkout System
- SQL Injection Testing for Security Learning

---

## 🎯 SQL Injection Demonstration
The purpose of this project is to **demonstrate SQL injection (SQLi)** by allowing malicious queries to be injected into login and other vulnerable forms.

✅ **Vulnerable Routes:**
- `/login` – Login with vulnerable query
- `/register` – Create a user without parameterized queries
- `/products` – Displaying products with unprotected query
- `/cart` – Fetching items with insecure query

---

## 🛠️ Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/belepod/Web-Application-Firewall.git
cd Web-Application-Firewall
```

## 2️⃣ Set Up a Virtual Environment
### Create virtual environment
`python3 -m venv venv`

## Activate the virtual environment
### On Linux/Mac
source venv/bin/activate
### On Windows
`venv\Scripts\activate`
## 3️⃣ Install Required Dependencies
`pip install -r requirements.txt`
## 🎮 Usage
### 🔥 Run the Application
`python app.py` : Web-App without WaF protection<br/>  
`python appwaf.py`  : Web-App with WaF protection<br/>  
`python standardwaf.py` : Only the WaF Inplementation (No Database)<br/>  
- Visit http://127.0.0.1:5000/ in your browser.
## 🧑‍💻 How to Perform SQL Injection
### 🛑 1️⃣ Bypass Login Authentication
Username: ' OR 1=1 --
Password: (any value)
✅ Outcome: Logs you in as the first user in the database.

### 🛑 2️⃣ Extract All User Credentials
Username: ' UNION SELECT id, username, password FROM users --
Password: (any value)
✅ Outcome: Displays all usernames and passwords.

### 🛑 3️⃣ Create an Admin User
Username: admin', 'hacked'); --
Password: (any value)
✅ Outcome: Adds an admin account to the database.

## 🔐 Security Recommendations
After demonstrating SQL injection vulnerabilities, secure the application by:

- Use Parameterized Queries (Prepared Statements)
- Prevent SQL injection by using placeholders.
- Hash Passwords Properly
- Use bcrypt or werkzeug.security for hashing.
- Implement a Web Application Firewall (WAF)
- Block malicious SQL and XSS payloads.
- Validate User Input
- Ensure input sanitization to block dangerous payloads.
