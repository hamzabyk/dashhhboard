import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def load_bist100_data():
    symbols = [
        ("ASELS", "Aselsan"), ("THYAO", "Türk Hava Yolları"), ("SISE", "Şişecam"),
        ("KRDMD", "Kardemir"), ("GARAN", "Garanti BBVA"), ("AKBNK", "Akbank"),
        ("FROTO", "Ford Otosan"), ("EREGL", "Ereğli Demir Çelik"), ("KCHOL", "Koç Holding"),
        ("TUPRS", "Tüpraş"), ("ISCTR", "İş Bankası"), ("VAKBN", "Vakıfbank"),
        ("YKBNK", "Yapı Kredi"), ("PGSUS", "Pegasus"), ("TAVHL", "TAV"),
        ("PETKM", "Petkim"), ("TOASO", "Tofaş"), ("HEKTS", "Hektaş"),
        ("SASA", "Sasa Polyester"), ("ALARK", "Alarko"), ("ENKAI", "Enka")
    ]
    rows = []
    for code, name in symbols:
        try:
            df = yf.Ticker(code + ".IS").history(period="5d")
            if df.empty: continue
            price = round(df['Close'][-1], 2)
            change = round(((df['Close'][-1] - df['Close'][-2]) / df['Close'][-2]) * 100, 2)
            rows.append({"Sembol": code, "Şirket": name, "Fiyat": price, "Değişim %": change})
        except:
            continue
    return pd.DataFrame(rows)

def get_graphs(symbol):
    ticker = yf.Ticker(symbol + ".IS")
    df = ticker.history(period="30d")
    if df.empty:
        return {"name": symbol, "price": 0, "change": 0, "volume": 0, "rsi": 0}, go.Figure(), go.Figure(), go.Figure()

    price = round(df['Close'][-1], 2)
    change = round(((df['Close'][-1] - df['Close'][-2]) / df['Close'][-2]) * 100, 2)
    volume = int(df['Volume'][-1])

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    rsi = round(100 - (100 / (1 + rs))[-1], 2)

    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=df.index, y=rs.where(rs.notna(), 0), mode='lines', name='RSI'))
    rsi_fig.update_layout(height=300, margin=dict(t=10, b=10), plot_bgcolor='#111', paper_bgcolor='#111', font=dict(color='white'))

    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Hacim'))
    vol_fig.update_layout(height=300, margin=dict(t=10, b=10), plot_bgcolor='#111', paper_bgcolor='#111', font=dict(color='white'))

    heat_fig = go.Figure()
    heat_fig.add_trace(go.Heatmap(z=[df['Close'].pct_change().fillna(0).tolist()], colorscale='RdBu'))
    heat_fig.update_layout(height=300, margin=dict(t=10, b=10), plot_bgcolor='#111', paper_bgcolor='#111', font=dict(color='white'))

    return {
        "name": symbol,
        "price": price,
        "change": change,
        "volume": volume,
        "rsi": rsi
    }, rsi_fig, vol_fig, heat_fig
