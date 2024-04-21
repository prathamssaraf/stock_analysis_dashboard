import sqlite3
import pandas as pd
import plotly.graph_objs as go

def fetch_yearly_data():
    conn = sqlite3.connect('M&M.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM yearly_data where Category != 'Depreciation' AND Category != 'OPM %' AND Category != 'Dividend Payout %' AND Category != 'EPS in Rs' AND Category != 'Tax %'")
    data = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    conn.close()
    return headers, data

def convert_yearly_to_dataframe():
    headers, data = fetch_yearly_data()
    df = pd.DataFrame(data, columns=headers)
    df.iloc[:, 1:] = df.iloc[:, 1:].replace({'%': '', ',': '', '': '0'}, regex=True).astype(float)
    return df

# Function to create line chart
def create_yearly_line_chart():
    df = convert_yearly_to_dataframe()
    # Assuming the first column contains the x-axis labels (months)
    x = df.columns[1:]  
    data = []
    for index, row in df.iterrows():
        # Assuming the first column contains the category names
        category_name = row[0]
        y = row[1:]  # Assuming the rest of the columns contain the y-axis values
        trace = go.Scatter(x=x, y=y, mode='lines+markers', name=category_name)
        data.append(trace)

    layout = go.Layout(
        title='Sales and Profit',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Value'),
        margin=dict(l=0, r=0, t=50, b=0),
        height=400,
        width=700
    )

    fig = go.Figure(data=data, layout=layout)
    return fig.to_json()
