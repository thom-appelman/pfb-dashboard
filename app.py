import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input

# Load provided dataset
df = pd.read_csv("https://raw.githubusercontent.com/thom-appelman/pfb-dashboard/main/customer_segmentation.csv")

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(children="Customer Segmentation Dashboard - by Thom Appelman"),
    html.Div([
        dcc.Dropdown(
            id="xaxis-job",
            options=[dict(label=i, value=i) for i in df["job_title"].unique()],
            value=["Nurse"],
            multi=True
        )
    ]),
    html.Div([
        dcc.Graph(id="job-barchart"),
        html.P(id="total-customers"),
        dcc.Graph(id="gender-piechart"),
        dcc.Graph(id="department-piechart")
    ]),
    html.Div([
        dcc.RadioItems(
            id="countries-toggle",
            options=[
                {'label': 'Top 5 countries (highest)', 'value': 'highest'},
                {'label': 'Top 5 countries (lowest)', 'value': 'lowest'}
            ],
            value="highest"
        )
    ]),
    dcc.Graph(id="countries-barchart"),
    html.Div([
        dcc.Dropdown(
            id="xaxis-country",
            options=[dict(label=i, value=i) for i in df["country"].unique()],
            value="United Kingdom"
        )
    ]),
    dcc.Graph(id="city-barchart")
])


@app.callback(
    Output("job-barchart", "figure"),
    Input("xaxis-job", "value"))
def update_job_barchart(xaxis_column_names):
    filtered_df = df[df["job_title"].isin(xaxis_column_names)]
    fig = px.histogram(filtered_df, x="job_title", title="Customers by profession",
                       labels=dict(x="Job title", y="Number of customers"))
    return fig

@app.callback(
    Output("total-customers", "children"),
    Input("xaxis-job", "value")
)

def update_total_customers(xaxis_column_names):
    filtered_df = df[df["job_title"].isin(xaxis_column_names)]
    total_customers = len(filtered_df)
    return f"Total number of customers based on Job selection: {total_customers}"

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
                       title="Top 5 countries highest/lowest number of customers",
                       labels=dict(x="Countries", y="Number of Customers"))
    return fig


@app.callback(
    Output("department-piechart", "figure"),
    Input("xaxis-job", "value")
)
def update_department_chart(xaxis_column_names):
    filtered_df = df[df["job_title"].isin(xaxis_column_names)]
    department_count = filtered_df["department"].value_counts()
    fig = px.pie(names=department_count.index, values=department_count.values,
                 title="Count of department of customer professions")
    return fig


@app.callback(
    Output("city-barchart", "figure"),
    Input("xaxis-country", "value")
)
def update_city_chart(xaxis_column_names):
    filtered_df = df[df["country"] == xaxis_column_names]
    city_count = filtered_df["city"].value_counts()
    top_five = city_count.head(5)
    fig = px.histogram(x=top_five.index, y=top_five.values, title="Number of customers by city in selected Country",
                       labels=dict(x="City", y="Number of customers"))
    return fig


# Run Dashboard application
if __name__ == "__main__":
    app.run_server(debug=True)
