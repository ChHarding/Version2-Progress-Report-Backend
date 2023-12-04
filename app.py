from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import stripe
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
YOUR_DOMAIN = 'http://127.0.0.1:4242'

app = Flask(__name__, template_folder='templates',
                      static_folder='static')

# Load the cleaned data into a pandas dataframe
df = pd.read_excel('ecommerce_clothing.xlsx')  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        # Get the search query and filter values from the form
        search_query = request.form['search_query']
        max_price = request.form['max_price']
        min_rating = request.form['min_rating']
        
        # Filter the dataframe based on the search query and filter values
        filtered_df = df[df['product_name'].str.contains(search_query, case=False)]
        if max_price:
            filtered_df = filtered_df[filtered_df['price'] <= float(max_price)]
        if min_rating:
            filtered_df = filtered_df[filtered_df['average_review_rating'] >= float(min_rating)]
        
        # Render the template with the filtered dataframe (sorted by rating and price)
        filtered_df = filtered_df.sort_values(['average_review_rating', 'price'], ascending=[False, True])
        return render_template('index.html', products=filtered_df.to_dict('records'),
                               search=search_query, max_price=max_price, min_rating=min_rating)

    else:
        # Render the template with no dataframe at the start
        template =render_template('index.html')
        return template

@app.route('/checkout', methods=['POST'])
def create_checkout_session():

    # get product_name and price from form in selection table
    product_name = request.form['product_name']
    unit_amount = int(float(request.form['price']) * 100) # in cents!
    image_url = "https://media.istockphoto.com/id/178851955/photo/flowery-evase-bateau-yellow-dress.jpg?s=2048x2048&w=is&k=20&c=g_vtLtL-644fOzFD2UulMORKDRhNN0bkKVHp9L1cByM="  #request.form['image_name']

    #create product for this name (stripe will give it a unique ID) and price for that product
    #product = stripe.Product.create(name=product_name) # product object
      
    product = stripe.Product.create(
        name=product_name,
        images=[image_url],   
    )

    price = stripe.Price.create(
        product=product.id,
        unit_amount=unit_amount,
        currency='usd'
    )

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the id of the Price object (which is also linked to the product, i.e. knows its name)
                    'price': price.id, # in cents!
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            #cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


if __name__ == '__main__':
    app.run(debug=False, port=4242)
