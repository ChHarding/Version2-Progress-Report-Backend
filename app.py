from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the cleaned data into a pandas dataframe
df = pd.read_excel('/Users/khinezaw/Documents/MHCI/E-Commerce-Clothing-Version2/Version2-Progress-Report-Backend/ecommerce_clothing.xlsx')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
        return render_template('index.html', products=filtered_df.to_dict('records'))
    else:
        # Render the template with no dataframe at the start
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)