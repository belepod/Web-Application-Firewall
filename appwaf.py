from flask import Flask, render_template, request, redirect, session, flash, abort
import mysql.connector
from config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'key'

def is_malicious_input(data):
    dangerous_patterns = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(;|--|\b(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC)\b)",
        r"(<script.*?>.*?</script>)",
        r"(<.*?javascript:.*?>)",
        r"(<iframe.*?>)",
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, data, re.IGNORECASE):
            return True
    return False

@app.before_request
def waf_protection():
    for key, value in {**request.args, **request.form}.items():
        if is_malicious_input(value):
            flash("Malicious activity detected, Request blocked.", "danger")
            abort(403)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect('/login')
        except mysql.connector.IntegrityError:
            flash("Username already exists!", "danger")

        cursor.close()
        conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect('/products')
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Logged out successfully!", "info")
    return redirect('/login')

@app.route('/')
def home():
    return redirect('/login')

@app.route('/products')
def products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash("Please log in to add items to the cart!", "warning")
        return redirect('/login')

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash("Product added to cart!", "success")
    return redirect('/products')

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash("Please log in to view your cart!", "warning")
        return redirect('/login')

    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', cart_items=[], total=0)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    product_ids = session['cart'].keys()
    if not product_ids:
        return render_template('cart.html', cart_items=[], total=0)

    placeholders = ','.join(['%s'] * len(product_ids))
    query = f"SELECT * FROM products WHERE id IN ({placeholders})"
    
    cursor.execute(query, tuple(product_ids))
    products = cursor.fetchall()
    
    total = 0
    cart_items = []
    for product in products:
        product['quantity'] = session['cart'][str(product['id'])]
        product['subtotal'] = product['quantity'] * product['price']
        total += product['subtotal']
        cart_items.append(product)

    cursor.close()
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'cart' in session:
        session.pop('cart')
    flash("Purchase successful! Thank you for shopping.", "success")
    return redirect('/products')

if __name__ == '__main__':
    app.run(debug=True)
