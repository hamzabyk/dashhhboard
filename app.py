import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from data_utils import load_bist100_data, get_graphs
import os

external_stylesheets = [dbc.themes.CYBORG]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

bist_df = load_bist100_data()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("\ud83d\udcca BIST 100", className="text-white mb-3"),
            dcc.Input(id="search-input", placeholder="Hisse ara...", type="text", className="mb-2", debounce=True),
            html.Div(id="stock-list", style={"overflowY": "auto", "height": "80vh"})
        ], width=3, style={"backgroundColor": "#1a1a1a", "padding": "1rem"}),

        dbc.Col([
            html.Div(id="stock-detail"),
            dcc.Tabs([
                dcc.Tab(label="RSI", children=[dcc.Graph(id="rsi-graph")]),
                dcc.Tab(label="Hacim", children=[dcc.Graph(id="volume-graph")]),
                dcc.Tab(label="Is\u0131 Haritas\u0131", children=[dcc.Graph(id="heat-graph")])
            ])
        ], width=9)
    ])
], fluid=True)

@app.callback(
    Output("stock-list", "children"),
    Input("search-input", "value")
)
def update_stock_list(query):
    filtered = bist_df.copy()
    if query:
        filtered = filtered[filtered["Sembol"].str.contains(query.upper()) | filtered["Şirket"].str.contains(query, case=False)]
    items = []
    for _, row in filtered.iterrows():
        items.append(html.Div([
            html.Div(f"{row['Sembol']} \u2013 {row['Şirket']}", className="text-white fw-bold"),
            html.Div(f"Fiyat: {row['Fiyat']} | %: {row['De\u011fi\u015fim %']}", className="text-muted small"),
        ], style={"padding": "10px", "borderBottom": "1px solid #333", "cursor": "pointer"},
        n_clicks=0,
        id={"type": "stock-item", "index": row["Sembol"]}))
    return items

@app.callback(
    Output("stock-detail", "children"),
    Output("rsi-graph", "figure"),
    Output("volume-graph", "figure"),
    Output("heat-graph", "figure"),
    Input({"type": "stock-item", "index": dash.ALL}, "n_clicks"),
    State({"type": "stock-item", "index": dash.ALL}, "id")
)
def update_detail(n_clicks_list, ids):
    if not any(n_clicks_list):
        return "", go.Figure(), go.Figure(), go.Figure()
    clicked = [i for i, n in enumerate(n_clicks_list) if n]
    if not clicked:
        return "", go.Figure(), go.Figure(), go.Figure()
    selected_symbol = ids[clicked[0]]["index"]
    info, rsi_fig, volume_fig, heat_fig = get_graphs(selected_symbol)
    detail = html.Div([
        html.H4(f"\ud83d\udccc {selected_symbol} \u2013 {info['name']}", className="text-info"),
        html.Div(f"Kapan\u0131\u015f: {info['price']} \u20ba", className="text-white"),
        html.Div(f"De\u011fi\u015fim: {info['change']}%", className="text-white"),
        html.Div(f"Hacim: {info['volume']:,}", className="text-white"),
        html.Div(f"RSI: {info['rsi']}", className="text-white"),
    ], className="mb-3")
    return detail, rsi_fig, volume_fig, heat_fig

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)
