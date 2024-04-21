from flask import Flask, render_template
from widgets.shareholding_pie_chart import create_pie_chart # type: ignore
from widgets.shareholding_line_chart import create_line_chart
from widgets.sales_line_chart import create_yearly_line_chart
from widgets.market_price_line_chart import fetch_company_data
from widgets.pe_card import fetch_pe
from widgets.market_cap_card import fetch_market_cap
from widgets.price_chart import plot_stock_price

app = Flask(__name__)

# Route for the dashboard page
@app.route('/')
def dashboard():

    # current market price card
    market_price = fetch_company_data()
    
    #stock pe card
    pe = fetch_pe()

    # market cap card
    market_cap = fetch_market_cap()

    #price history line chart
    price_chart = plot_stock_price('M&M.NS', '1yr')

    # shareholding pie chart
    pie_chart_json = create_pie_chart()

    # shareholding history line chart
    line_chart_json = create_line_chart()

    # Create yearly bar chart
    sales_yearly_json = create_yearly_line_chart()

    
    

    # Render the dashboard template with the chart JSONs
    return render_template('index.html', 
                           pie_chart_json=pie_chart_json, 
                           line_chart_json=line_chart_json, 
                           sales_yearly_json=sales_yearly_json,
                           market_price=market_price,
                           pe = pe,
                           market_cap=market_cap,
                           price_chart=price_chart)

if __name__ == '__main__':
    app.run(debug=True)
