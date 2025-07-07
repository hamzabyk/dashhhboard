from dash import ALL
from dash import Dash, dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import os
from data_utils import load_bist100_data, get_graphs
from currency_widget import get_currency_widget

external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

data = load_bist100_data()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("📋 Hisseler", className="text-white mb-3"),
            dcc.Input(id="search-input", placeholder="Hisse ara...", debounce=True, className="mb-2"),
            html.Div(id="stock-list", style={"overflowY": "auto", "height": "75vh"})
        ], width=3, style={"backgroundColor": "#1a1a1a", "padding": "1rem"}),

        dbc.Col([
            html.Div(id="stock-detail"),
            dcc.Tabs([
                dcc.Tab(label="RSI", children=[dcc.Graph(id="rsi-graph")]),
                dcc.Tab(label="Hacim", children=[dcc.Graph(id="volume-graph")]),
                dcc.Tab(label="Isı Haritası", children=[dcc.Graph(id="heat-graph")])
            ])
        ], width=9)
    ]),
    html.Div(get_currency_widget(), style={"position": "fixed", "bottom": "10px", "right": "20px", "zIndex": "999"})
], fluid=True)

@app.callback(
    Output("stock-list", "children"),
    Input("search-input", "value")
)
def update_stock_list(query):
    filtered = data.copy()
    if query:
        filtered = filtered[filtered["Sembol"].str.contains(query.upper()) | filtered["Şirket"].str.contains(query, case=False)]
    items = []
    for _, row in filtered.iterrows():
        items.append(html.Div([
            html.Div(f"{row['Sembol']} – {row['Şirket']}", className="text-white fw-bold"),
            html.Div(f"Fiyat: {row['Fiyat']} | %: {row['Değişim %']}", className="text-muted small"),
        ], style={"padding": "10px", "borderBottom": "1px solid #333", "cursor": "pointer"},
        id={"type": "stock-item", "index": row["Sembol"]}))
    return items

@app.callback(
    Output("stock-detail", "children"),
    Output("rsi-graph", "figure"),
    Output("volume-graph", "figure"),
    Output("heat-graph", "figure"),
    Input({"type": "stock-item", "index": ALL}, "n_clicks"),
    State({"type": "stock-item", "index": ALL}, "id")
)
def update_detail(n_clicks, ids):
    triggered = ctx.triggered_id
    if not triggered:
        return "", go.Figure(), go.Figure(), go.Figure()
    selected_symbol = triggered["index"]
    info, rsi_fig, volume_fig, heat_fig = get_graphs(selected_symbol)
    detail = html.Div([
        html.H4(f"📌 {selected_symbol} – {info['name']}", className="text-info"),
        html.Div(f"Kapanış: {info['price']} ₺", className="text-white"),
        html.Div(f"Değişim: {info['change']}%", className="text-white"),
        html.Div(f"Hacim: {info['volume']:,}", className="text-white"),
        html.Div(f"RSI: {info['rsi']}", className="text-white"),
    ], className="mb-3")
    return detail, rsi_fig, volume_fig, heat_fig

