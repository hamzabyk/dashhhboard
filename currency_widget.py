import yfinance as yf
from dash import html

def get_currency_widget():
    pairs = [
        ("USDTRY=X", "USD/TRY"),
        ("EURTRY=X", "EUR/TRY"),
        ("GBPTRY=X", "GBP/TRY")
    ]
    items = []
    for symbol, label in pairs:
        try:
            price = round(yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1], 2)
            items.append(html.Div(f"{label}: {price} ₺", className="text-white small"))
        except:
            items.append(html.Div(f"{label}: veri yok", className="text-danger small"))
    return html.Div(items, style={
        "backgroundColor": "#1a1a1a",
        "padding": "10px",
        "border": "1px solid #444",
        "borderRadius": "5px"
    })
