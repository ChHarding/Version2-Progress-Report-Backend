from flask import Flask, render_template, request
import pandas as pd
import stripe
import os

from keys import SECRET_KEY, PUBLISHABLE_KEY

#stripe.api_key = stripe_keys['secret_key']
stripe.api_key = SECRET_KEY

app = Flask(__name__, template_folder='templates',
                      static_folder='static')

# Load the cleaned data into a pandas dataframe
df = pd.read_excel('ecommerce_clothing.xlsx') # CH this started with /  !!!!

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
        return render_template('index_CH.html', products=filtered_df.to_dict('records'), search=search_query, max_price=max_price, min_rating=min_rating)

    else:
        # Render the template with no dataframe at the start
        template =render_template('index_CH.html')
        return template

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)


if __name__ == '__main__':
    app.run(debug=False)
