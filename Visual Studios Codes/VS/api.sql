from flask import Flask, jsonify, request
from helper import execute_query

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#home page of the website
@app.route('/')
def homepage():
    return (
        '<center><b><h1>Welcome to DesigNest!</h1></b></center>'
        '<b><h2>Use: /signup</h2></b><br><br>'
        '<b><h2>Use: /login</h2></b><br><br>'
        '<b><h3>Use: /user/< int:id ></h3></b><br><br>'
        '<b><h4>Use: /product-collection</h4></b><br><br>'
        '<b><h4>Use: /product-clothing</h4></b><br><br>'
        '<b><h5>Use: /view-cart</h5></b>'
    )

#Signup page
@app.route('/signup', methods=['POST'])
def signup_user():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        location = data.get('location')
        state = data.get('state')

        if not all([name, email, password, location, state]):
            return jsonify({'error': 'Missing required fields'}), 400

        query = f"INSERT INTO customer_table (name, email, password, location, state) VALUES ('{name}', '{email}', '{password}', '{location}', '{state}')"
        execute_query(query)
        return jsonify({'message': 'User signed up successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Login page
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data['email']
    password = data['password']

    query = "SELECT * FROM customer_table WHERE email = %s AND password = %s"
    result = execute_query(query, (email, password))

    if result:
        return jsonify({'message': 'Login successful!', 'user': result})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

#user profile
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = execute_query(f"SELECT * FROM customer_table WHERE customer_id = {id}")
    if user:
        return jsonify(user)
    else:
        return jsonify({'message: No matching user found'})

#product details from collection table
@app.route('/product-collection', methods=['GET'])
def product_collection():
    product = execute_query("SELECT * FROM collection_table")
    return jsonify(product)

#product details
@app.route('/product-clothing', methods=['GET'])
def product_clothing():
    product = execute_query("SELECT * FROM  clothing_item_table")
    return jsonify(product)

#view cart
@app.route('/view-cart/<int:id>', methods=['GET'])
def view_cart(id):
    # Fetch the cart details for the customer
    cart_query = "SELECT * FROM cart_table WHERE customer_id = {}".format(id)
    cart = execute_query(cart_query)
    
    if cart:
        return jsonify(cart)
    else:
        return '<h1 style= "font-size: 56px;">No customer found</h1>' , 404


if __name__ == '__main__':
    app.run(debug = False)