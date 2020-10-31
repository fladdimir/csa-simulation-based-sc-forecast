import os
from datetime import date
from typing import Tuple

import boto3
import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from data_loader import load_data

"""
aws setup:
    export AWS_ENDPOINT=http://localhost:4566
    export TABLE_NAME=analytics_table
    export AWS_DEFAULT_REGION=localhost
    export AWS_ACCESS_KEY_ID=access_key_id
    export AWS_SECRET_ACCESS_KEY=secret_access_key
"""

if "AWS_DEFAULT_REGION" not in os.environ:
    os.environ["AWS_DEFAULT_REGION"] = "localhost"
if "AWS_ACCESS_KEY_ID" not in os.environ:
    os.environ["AWS_ACCESS_KEY_ID"] = "access_key_id"
if "AWS_SECRET_ACCESS_KEY" not in os.environ:
    os.environ["AWS_SECRET_ACCESS_KEY"] = "secret_access_key"

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
TABLE_NAME = os.getenv("TABLE_NAME", "analytics_table")

dynamodb = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT)
table = dynamodb.Table(TABLE_NAME)

auto_update = True


def create_interval_component(enabled=True):
    # polling is bad
    disabled = not enabled
    return dcc.Interval(
        id="interval_component", interval=1000, n_intervals=0, disabled=disabled
    )


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    children=[
        html.H3(children="Example Dashboard"),
        daq.ToggleSwitch(id="auto_update_toggle", value=True, label="auto-update"),
        dcc.Graph(id="example_graph"),
        html.Div(
            id="interval_parent",
            children=create_interval_component(enabled=auto_update),
        ),
    ],
)


def load_data_from_db() -> Tuple[pd.DataFrame, date, date]:
    return load_data(table)


colors = {
    "production": "rgb(0, 255, 0)",
    "queued": "rgb(255, 0, 0)",
    "material delivery": "rgb(0, 0, 255)",
    "material delivery delay": "rgb(255, 165, 0)",
}


def create_graph(df: pd.DataFrame, current_time, last_update):
    figure = px.timeline(
        df,
        x_start="start",
        x_end="finish",
        y="task",
        color="resource",
        color_discrete_map=colors,
        title=f"Current time: {current_time}  -  Forecast until: {last_update}",
    )
    figure.add_vline(x=current_time)
    return figure


@app.callback(
    Output("example_graph", "figure"), [Input("interval_component", "n_intervals")]
)
def update_graph_live(_):
    df, current_time, last_update = load_data_from_db()
    return create_graph(df, current_time, last_update)


@app.callback(
    Output("interval_parent", "children"),
    [Input("auto_update_toggle", "value")],
)
def update_output(value):
    return create_interval_component(value)


if __name__ == "__main__":
    app.run_server(debug=True)
