import dash
from dash import dcc, html, Input, Output
import sqlite3
import pandas as pd

# Function to fetch data from the company_data table
def fetch_company_data():
    conn = sqlite3.connect('M&M.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM company_data WHERE field = 'Current Price'")
    current_price = cursor.fetchone()[0]
    conn.close()
    return current_price


