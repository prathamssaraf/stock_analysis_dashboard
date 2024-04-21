import sqlite3
import pandas as pd
import plotly.graph_objs as go

# Function to fetch data from the database
def fetch_line_data():
    conn = sqlite3.connect('M&M.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shareholding_quarterly_data WHERE category != 'No. of Shareholders'")
    data = cursor.fetchall()
    headers = [description[0] for description in cursor.description]  # Fetch column names
    conn.close()
    return headers, data

# Convert fetched data to DataFrame
def convert_to_dataframe():
    headers, data = fetch_line_data()
    df = pd.DataFrame(data, columns=headers)
    # Remove '%' symbol and convert to float
    df.iloc[:, 1:] = df.iloc[:, 1:].replace({'%': ''}, regex=True).astype(float)
    return df

# Function to create line chart
def create_line_chart():
    df = convert_to_dataframe()
    # Assuming the first column contains the x-axis labels (months)
    x = df.columns[1:]  
    data = []
    for index, row in df.iterrows():
        # Assuming the first column contains the category names
        category_name = row[0]
        if category_name == 'No. of Shareholders':
            continue  # Skip plotting "No. of Shareholders" data
        y = row[1:]  # Assuming the rest of the columns contain the y-axis values
        trace = go.Scatter(x=x, y=y, mode='lines+markers', name=category_name)
        data.append(trace)

    layout = go.Layout(
        title='Shareholding Pattern TimeLine',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Value', range=[0, 50], dtick=10),
        margin=dict(l=0, r=0, t=50, b=0),
        height=400,
        width=700
    )

    fig = go.Figure(data=data, layout=layout)
    return fig.to_json()
