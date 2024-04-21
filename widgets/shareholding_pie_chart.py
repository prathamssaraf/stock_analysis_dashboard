import sqlite3
import plotly.graph_objs as go

def fetch_pie_data():
    conn = sqlite3.connect('M&M.db')
    cursor = conn.cursor()
    cursor.execute("SELECT category, [Mar 2024] FROM shareholding_yearly_data WHERE category != 'No. of Shareholders'")
    data = cursor.fetchall()
    conn.close()
    return data

def create_pie_chart():
    data = fetch_pie_data()

    categories = [row[0] for row in data]
    values = [float(row[1].rstrip('%')) for row in data]

    total_sum = sum(values)

    percentages = [(value / total_sum) * 100 for value in values]

    pie_chart = go.Pie(
        labels=categories,  
        values=percentages,  
        hole=0.3,
    )

    layout = go.Layout(
        title="Shareholding Distribution - Mar 2024",
        height=400,
        width=330,
        margin=dict(l=50, r=50, t=50, b=50),
        showlegend=True,
        legend=dict(x=-0.3, y=-0.4),
    )

    pie_chart_div = go.Figure(data=pie_chart, layout=layout)

    pie_chart_json = pie_chart_div.to_json()

    return pie_chart_json
