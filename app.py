import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input

# Load provided dataset
df = pd.read_csv("https://raw.githubusercontent.com/thom-appelman/pfb-dashboard/main/customer_segmentation.csv")

app = Dash(__name__)
app.title = "Customer Segmentation Dashboard"
server = app.server

app.layout = html.Div([
    html.Div(
        children=[
            html.H1("Customer Segmentation Dashboard", style={"color": "white", "textAlign": "center"}),
            html.H4("Created by Thom P.J. Appelman - S5502577", style={"color": "white", "textAlign": "center"}),
        ],
        style={
            "backgroundColor": "#1F559F",
            "padding": "5px",
            "marginBottom": "10px",
        }
    ),
    html.Div([
        html.H4("Select professions from the drop-down list"),
        dcc.Dropdown(
            id="xaxis-job",
            options=[dict(label=i, value=i) for i in df["job_title"].unique()],
            value=["Nurse"],
            multi=True
        )
    ]),
    html.Div([
        dcc.Graph(id="job-barchart"),
        html.H3(id="total-customers", style={"textAlign": "center"}),
    ]),
    html.Div([
        dcc.Graph(id="gender-piechart"),
        html.H4("Select a gender to see the breakdown of departments"),
        dcc.Dropdown(
            id="dropdown-gender",
            options=[dict(label=i, value=i) for i in df["gender"].unique()],
            value="Male"),
        dcc.Graph(id="department-piechart")
    ]),
    html.Div([
        html.H4("Show top 5 countries with:"),
        dcc.RadioItems(
            id="countries-toggle",
            options=[
                {"label": "Highest number of customers", "value": "highest"},
                {"label": "Lowest number of customers", "value": "lowest"}
            ],
            value="highest")
    ]),
    dcc.Graph(id="countries-barchart"),
    html.Div([
        html.H4("Top cities based on the number of customers in:"),
        dcc.Dropdown(
            id="xaxis-country",
            options=[dict(label=i, value=i) for i in df["country"].unique()],
            value="United Kingdom"
        )
    ]),
    dcc.Graph(id="city-barchart")
], style={'font-family': 'Arial'})


# Bar chart showing number of customers based on drop-down list of job titles
@app.callback(
    Output("job-barchart", "figure"),
    Input("xaxis-job", "value"))
def update_job_barchart(xaxis_column_names):
    filtered_df = df[df["job_title"].isin(xaxis_column_names)]
    fig = px.histogram(filtered_df, x="job_title", title="Customers by profession",
                       labels={"job_title": "Profession", "count": "Number of Customers"},
                       color="job_title", template="simple_white")
    return fig


# Showing the total number of customers based on job title selection
@app.callback(
    Output("total-customers", "children"),
    Input("xaxis-job", "value")
)
def update_total_customers(xaxis_column_names):
    filtered_df = df[df["job_title"].isin(xaxis_column_names)]
    total_customers = len(filtered_df)
    return f"Total number of customers based on Job selection: {total_customers}"


# Pie chart showing department breakdown for selected gender
@app.callback(
    Output("gender-piechart", "figure"),
    Input("xaxis-job", "value")
)
def update_gender_pie(xaxis_column_names):
    filtered_df = df[df["job_title"].isin(xaxis_column_names)]
    gender_count = filtered_df["gender"].value_counts()
    fig = px.pie(names=gender_count.index, values=gender_count.values,
                 title="gender breakdown of customers by selected professions")
    return fig


# Histogram showing the top 5 or bottom 5 countries based on number of customers
@app.callback(
    Output("countries-barchart", "figure"),
    Input("countries-toggle", "value")
)
def update_country_chart(order):
    countries_count = df["country"].value_counts()
    if order == "highest":
        top_five = countries_count.head(5)
    else:
        top_five = countries_count.tail(5)
    fig = px.histogram(x=top_five.index, y=top_five.values,
                       title=f"Top 5 countries with the {order} number of customers",
                       labels=dict(x="Countries", y="Number of Customers"),
                       color=top_five.index, template="simple_white")
    return fig


# Pie chart showing the breakdown of departments based on selected gender
@app.callback(
    Output("department-piechart", "figure"),
    Input("dropdown-gender", "value")
)
def update_department_pie(gender):
    filtered_df = df[df["gender"] == gender]
    department_count = filtered_df["department"].value_counts()
    fig = px.pie(names=department_count.index, values=department_count.values,
                 title=f"Breakdown of departments for {gender} customers")
    return fig


# Bar chart showing the 10 cities with the most customers from the selected countries
@app.callback(
    Output("city-barchart", "figure"),
    Input("xaxis-country", "value")
)
def update_city_chart(xaxis_column_names):
    filtered_df = df[df["country"] == xaxis_column_names]
    city_count = filtered_df["city"].value_counts()
    top_cities = city_count.head(10)
    fig = px.histogram(x=top_cities.index, y=top_cities.values,
                       title=f"Top Cities by number of customers in {xaxis_column_names}",
                       labels=dict(x="City", y="Number of customers"),
                       color=top_cities.index, template="simple_white")
    return fig


# Run Dashboard application
if __name__ == "__main__":
    app.run_server()
