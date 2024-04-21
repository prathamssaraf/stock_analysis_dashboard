from flask import Flask, render_template
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

def plot_stock_price(symbol, duration):
    # Determine the start date based on the duration
    if duration == '1yr':
        start_date = datetime.now() - timedelta(days=365)
    elif duration == '2yr':
        start_date = datetime.now() - timedelta(days=365*2)
    elif duration == '5yr':
        start_date = datetime.now() - timedelta(days=365*5)
    else:
        print("Invalid duration. Please choose from '1yr', '2yr', or '5yr'.")
        return None

    # Fetch historical stock data for the specified duration
    stock_data = yf.download(symbol, start=start_date, end=datetime.now())

    # Create a trace for the closing prices
    trace = go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=symbol)

    # Create layout
    layout = go.Layout(title=f'\tPrice Chart',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Price'),
                       hovermode='closest',
                       margin=dict(l=0, r=0, t=50, b=0),
                       height=370,
                       width=550,
                       showlegend=False)

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)

    return fig.to_json()