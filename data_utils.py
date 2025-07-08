
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def get_bist30_index_figure():
    try:
        df = yf.download("^XU030", period="1mo", interval="1d")  # BIST30 Endeksi
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="BIST30"))
        fig.update_layout(
            title="BIST 30 Endeksi (XU030)",
            xaxis_title="Tarih",
            yaxis_title="Kapanış Fiyatı",
            template="plotly_dark",
            height=300
        )
        return fig
    except Exception as e:
        print("BIST30 veri hatası:", e)
        return go.Figure()
        
def load_bist100_data():
    symbols = [
        ("AKBNK", "Akbank"),
        ("ARCLK", "Arçelik"),
        ("ASELS", "Aselsan"),
        ("BIMAS", "Bim"),
        ("EKGYO", "Emlak GYO"),
        ("EREGL", "Ereğli Demir Çelik"),
        ("FROTO", "Ford Otosan"),
        ("GARAN", "Garanti BBVA"),
        ("GUBRF", "Gübretaş"),
        ("HEKTS", "Hektaş"),
        ("ISCTR", "İş Bankası"),
        ("KCHOL", "Koç Holding"),
        ("KRDMD", "Kardemir D"),
        ("KOZAA", "Koza Altın"),
        ("KOZAL", "Koza Madencilik"),
        ("PGSUS", "Pegasus"),
        ("PETKM", "Petkim"),
        ("SAHOL", "Sabancı Holding"),
        ("SASA", "Sasa Polyester"),
        ("SISE", "Şişecam"),
        ("TCELL", "Turkcell"),
        ("THYAO", "THY"),
        ("TKFEN", "Tekfen"),
        ("TOASO", "Tofaş"),
        ("TUPRS", "Tüpraş"),
        ("VAKBN", "Vakıfbank"),
        ("YKBNK", "Yapı Kredi"),
        ("TAVHL", "TAV Havalimanları"),
        ("ALARK", "Alarko"),
        ("ENKAI", "Enka İnşaat")
    ]

    rows = []
    for symbol, name in symbols:
        try:
            df = yf.Ticker(symbol + ".IS").history(period="5d")
            if df.empty:
                continue
            price = round(df["Close"].iloc[-1], 2)
            change = round(((df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]) * 100, 2)
            rows.append({"Sembol": symbol, "Şirket": name, "Fiyat": price, "Değişim %": change})
        except:
            continue
    return pd.DataFrame(rows)

def get_graphs(symbol):
    df = yf.Ticker(symbol + ".IS").history(period="30d")
    if df.empty:
        return {"name": symbol, "price": 0, "change": 0, "volume": 0, "rsi": 0}, go.Figure(), go.Figure(), go.Figure()

    price = round(df["Close"].iloc[-1], 2)
    change = round(((df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]) * 100, 2)
    volume = int(df["Volume"].iloc[-1])

    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    rsi = round(100 - (100 / (1 + rs))[-1], 2)

    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=df.index, y=rs.where(rs.notna(), 0), mode='lines', line=dict(color='#3b82f6')))
    rsi_fig.update_layout(plot_bgcolor='#1a1a1a', paper_bgcolor='#1a1a1a', font_color='white', height=300)

    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(x=df.index, y=df["Volume"], marker=dict(color="#3b82f6")))
    vol_fig.update_layout(plot_bgcolor='#1a1a1a', paper_bgcolor='#1a1a1a', font_color='white', height=300)

    heat_fig = go.Figure()
    heat_fig.add_trace(go.Heatmap(z=[df["Close"].pct_change().fillna(0).tolist()], colorscale='RdBu'))
    heat_fig.update_layout(plot_bgcolor='#1a1a1a', paper_bgcolor='#1a1a1a', font_color='white', height=300)

    return {
        "name": symbol,
        "price": price,
        "change": change,
        "volume": volume,
        "rsi": rsi
    }, rsi_fig, vol_fig, heat_fig

def load_bist30_index_graph():
    df = pd.read_csv("data/bist30.csv", parse_dates=["Tarih"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Tarih"], y=df["Kapanış"], mode="lines", name="BIST30"))
    fig.update_layout(
        title="📈 BIST30 Endeksi",
        paper_bgcolor="#1a1a1a",
        plot_bgcolor="#1a1a1a",
        font=dict(color="#FFFFFF"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return fig



