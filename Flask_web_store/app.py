#app.py
from flask import Flask, session, render_template, request, redirect, url_for
#import psycopg2 #pip install psycopg2 
#import psycopg2.extras


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fintech_bootcamp_wine_chain'
 
#app.secret_key = "cairocoders-ednalan"
 
#DB_HOST = "localhost", DB_NAME = "sampledb", DB_USER = "postgres",DB_PASS = "admin"
#conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

items = [{ 'code': 'SKU-1', 
          'name': 'Caymus',
          'category': 'Wine',
          'image': 'Caymus.png',
          'price': 0.001},
        { 'code': 'SKU-2', 
          'name': 'Cakebread',
          'category': 'Wine',
          'image': 'Cakebread.png',
          'price': 0.0013},
        { 'code': 'SKU-3', 
          'name': 'Cott',
          'category': 'Wine',
          'image': 'Cott.png',
          'price': 0.0007},
        { 'code': 'SKU-4', 
          'name': 'Artemis',
          'category': 'Wine',
          'image': 'Artemis.png',
          'price': 0.0008}   
        ]

@app.route('/')
def products():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    #cursor.execute("SELECT * FROM product")
    #rows = cursor.fetchall()
    
    return render_template('products.html', products=items)


@app.route('/add', methods=['POST'])
def add_product_to_cart():
    _quantity = int(request.form['quantity'])
    _code = request.form['code']
    
    # validate the received values
    if _quantity and _code and request.method == 'POST':
 
        #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
        #cursor.execute('SELECT * FROM product WHERE code = %s', (_code,))
        #row = cursor.fetchone()
         
        row = next((sku for sku in items if sku['code'] == _code), None) 
         
        itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price': _quantity * row['price']}}
        
        all_total_price = 0
        all_total_quantity = 0
                 
        session.modified = True
        if 'cart_item' in session:
            if row['code'] in session['cart_item']:
                for key, value in session['cart_item'].items():
                    if row['code'] == key:
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + _quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * row['price']
            else:
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
         
            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
        else:
            session['cart_item'] = itemArray
            all_total_quantity = all_total_quantity + _quantity
            all_total_price = all_total_price + _quantity * row['price']
             
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price
        
        return redirect(url_for('products'))
    else:
        return 'Error while adding item to cart'
 

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)
 
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False

@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
         
        for item in session['cart_item'].items():
            if item[0] == code:    
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
         
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
             
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)
 
if __name__ == "__main__":
    app.run(debug=True)