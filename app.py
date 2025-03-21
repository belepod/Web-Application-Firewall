from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

# 🟢 Register Route
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

# 🟢 Login Route
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

# 🟢 Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Logged out successfully!", "info")
    return redirect('/login')

# 🟢 Home Route
@app.route('/')
def home():
    return redirect('/login')

# 🟢 Product List
@app.route('/products')
def products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products)

# 🟢 Add to Cart
@app.route('/add_to_cart/<int:product_id>')
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

# 🟢 View Cart
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
    cursor.execute(f"SELECT * FROM products WHERE id IN ({','.join(product_ids)})")
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

# 🟢 Checkout
@app.route('/checkout')
def checkout():
    if 'cart' in session:
        session.pop('cart')
    flash("Purchase successful! Thank you for shopping.", "success")
    return redirect('/products')

if __name__ == '__main__':
    app.run(debug=True)
