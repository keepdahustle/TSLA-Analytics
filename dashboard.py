import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import database initialization
from database import init_pool, close_all_connections
from data_accessor import DataAccessor

# Initialize database pool
try:
    init_pool()
except Exception as e:
    print(f"[ERROR] Failed to initialize database: {e}")
    raise

print("[DEBUG] Database pool initialized successfully")

# ── Colour System (Modern Light Fintech) ──────────────────────────────────
C_RED       = "#E63946"
C_RED_SOFT  = "#FF6B6B"
C_RED_BG    = "#FFF1F2"
C_RED_MUTED = "#FECDD3"
C_DARK      = "#1F2937"
C_MID       = "#374151"
C_GRAY      = "#6B7280"
C_BORDER    = "#E5E7EB"
C_BG        = "#F8FAFC"
C_CARD      = "#FFFFFF"
C_GREEN     = "#10B981"
C_GREEN_BG  = "#ECFDF5"
C_BLUE      = "#3B82F6"
C_BLUE_BG   = "#EFF6FF"
C_AMBER     = "#F59E0B"
C_AMBER_BG  = "#FFFBEB"
C_PURPLE    = "#8B5CF6"
C_CHART_BG  = "#FFFFFF"
C_GRID      = "#F3F4F6"

# ── Load data from PostgreSQL ────────────────────────────────────────────────
print("[DEBUG] Loading data from PostgreSQL...")

try:
    df = DataAccessor.get_tesla_stock_data().sort_values("Date")
    df["Year"]    = df["Date"].dt.year
    df["Quarter"] = df["Date"].dt.quarter
    df["Month"]   = df["Date"].dt.month
    print(f"[DEBUG] Loaded Tesla stock data: {len(df)} rows")
except Exception as e:
    print(f"[ERROR] Failed to load Tesla stock data: {e}")
    df = pd.DataFrame()

try:
    df_2023    = df[df["Year"] == 2023]
    df_2024    = df[df["Year"] == 2024]
    df_2024_q1 = df_2024[df_2024["Quarter"] == 1]
    print(f"[DEBUG] Filtered data: 2023={len(df_2023)}, 2024={len(df_2024)}, 2024 Q1={len(df_2024_q1)}")
except Exception as e:
    print(f"[ERROR] Failed to filter data: {e}")

# Load evaluation metrics
try:
    eval_df = DataAccessor.get_model_evaluation()
    print(f"[DEBUG] Loaded model evaluation: {len(eval_df)} rows, columns: {list(eval_df.columns)}")
except Exception as e:
    print(f"[ERROR] Failed to load model evaluation: {e}")
    eval_df = pd.DataFrame()

# Load predictions
model_preds = {}
for model_name, accessor in [("sarima", DataAccessor.get_predictions_sarima), 
                              ("prophet", DataAccessor.get_predictions_prophet)]:
    try:
        model_preds[model_name] = accessor()
        print(f"[DEBUG] Loaded {model_name} predictions: {len(model_preds[model_name])} rows, columns: {list(model_preds[model_name].columns)}")
    except Exception as e:
        print(f"[ERROR] Failed to load {model_name} predictions: {e}")

print(f"[DEBUG] Successfully loaded {len(model_preds)} prediction models")
print(f"[DEBUG] eval_df shape: {eval_df.shape}")

# ── News Data ─────────────────────────────────────────────────────────────
tesla_news = [
    {
        "date": "Jan 3, 2024",
        "source": "Reuters",
        "source_icon": "📡",
        "headline": "Tesla Q4 2023 Deliveries Beat Expectations: 484,507 Units",
        "summary": "Full-year 2023 deliveries reached 1.81 million vehicles, surging 38% year-over-year and surpassing analyst consensus forecasts.",
        "impact": "Positive",
        "url": "https://www.reuters.com/business/autos-transportation/tesla-delivers-record-1-81-mln-vehicles-2023-2024-01-03/",
        "tag": "Deliveries"
    },
    {
        "date": "Nov 30, 2023",
        "source": "Bloomberg",
        "source_icon": "📊",
        "headline": "Cybertruck Officially Delivered — Tesla's Most Anticipated Vehicle",
        "summary": "10 initial Cybertrucks handed over to customers; production ramp is expected to accelerate through 2024 with capacity targets of 250,000/year.",
        "impact": "Positive",
        "url": "https://www.bloomberg.com/news/articles/2023-11-30/tesla-begins-delivering-eagerly-awaited-cybertruck",
        "tag": "Product Launch"
    },
    {
        "date": "Nov 14, 2023",
        "source": "CNBC",
        "source_icon": "📺",
        "headline": "Cybertruck Delivery Event Confirmed for November 30",
        "summary": "Tesla officially confirms first Cybertruck customer deliveries, reigniting bullish sentiment after months of production delays.",
        "impact": "Positive",
        "url": "https://www.cnbc.com/2023/11/14/tesla-sets-cybertruck-delivery-date-november-30.html",
        "tag": "Announcement"
    },
    {
        "date": "Oct 18, 2023",
        "source": "Wall Street Journal",
        "source_icon": "📰",
        "headline": "Q3 Earnings: Margin Compression Persists Amid Global EV Price War",
        "summary": "Automotive gross margin fell to 17.9% driven by aggressive worldwide price reductions. Investors remain cautious on profitability outlook.",
        "impact": "Negative",
        "url": "https://www.wsj.com/articles/tesla-profit-squeezed-by-price-war-production-snafu-11697636408",
        "tag": "Earnings"
    },
    {
        "date": "Oct 2, 2023",
        "source": "Financial Times",
        "source_icon": "🗞️",
        "headline": "Tesla Q3 2023 Deliveries Miss Street Estimates",
        "summary": "Tesla delivered 435,059 vehicles in Q3, falling short of the consensus estimate of ~456,000 units. Supply chain concerns cited.",
        "impact": "Negative",
        "url": "https://www.ft.com/content/6c7ca0c9-c89e-4e5f-8e7c-9c3d7e8b4a3c",
        "tag": "Deliveries"
    },
]

# ── Helpers ───────────────────────────────────────────────────────────────
def chart_layout(title="", height=360):
    return dict(
        title=dict(text=title, font=dict(size=15, color=C_DARK, family="DM Sans, sans-serif"), x=0, xanchor="left", pad=dict(l=4, t=4)),
        paper_bgcolor=C_CHART_BG,
        plot_bgcolor=C_CHART_BG,
        font=dict(color=C_GRAY, family="DM Sans, sans-serif", size=12),
        height=height,
        margin=dict(l=10, r=10, t=48, b=10),
        xaxis=dict(showgrid=False, zeroline=False, linecolor=C_BORDER, tickfont=dict(size=11, color=C_GRAY)),
        yaxis=dict(showgrid=True, gridcolor=C_GRID, zeroline=False, linecolor=C_BORDER, tickfont=dict(size=11, color=C_GRAY)),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(size=12), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )

def card(children, padding="24px", style_extra=None):
    s = {
        "background": C_CARD,
        "borderRadius": "16px",
        "padding": padding,
        "marginBottom": "20px",
        "boxShadow": "0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04)",
        "border": f"1px solid {C_BORDER}",
    }
    if style_extra:
        s.update(style_extra)
    return html.Div(children, style=s)

def section_label(text):
    return html.Div([
        html.Span(style={"display":"inline-block","width":"4px","height":"18px","background":C_RED,"borderRadius":"2px","marginRight":"10px","verticalAlign":"middle"}),
        html.Span(text, style={"fontSize":"13px","fontWeight":"600","color":C_GRAY,"textTransform":"uppercase","letterSpacing":"0.08em","verticalAlign":"middle"})
    ], style={"marginBottom":"16px"})

# ── App ───────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="TSLA Analytics — Tesla Stock Intelligence")

SIDEBAR_W = "220px"

# Global font injection via app external stylesheets
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
        * { box-sizing: border-box; }
        body { margin: 0; background: #F8FAFC; font-family: 'DM Sans', sans-serif; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #F1F5F9; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
        .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important; }
        .nav-item:hover { background: #F1F5F9 !important; color: #1F2937 !important; }
        .nav-item.active { background: #FFF1F2 !important; color: #E63946 !important; }
        .news-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important; transform: translateY(-1px); }
        .tab-btn { transition: all 0.2s ease; }
        .tab-btn:hover { background: #F9FAFB; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def sidebar():
    nav_items = [
        ("📈", "Overview", "overview"),
        ("🔍", "EDA", "eda"),
        ("🤖", "AI Forecast", "predictions"),
        ("📰", "News Feed", "news"),
    ]
    return html.Div(style={
        "width": SIDEBAR_W, "minWidth": SIDEBAR_W,
        "background": C_CARD,
        "borderRight": f"1px solid {C_BORDER}",
        "height": "100vh",
        "position": "sticky",
        "top": "0",
        "display": "flex",
        "flexDirection": "column",
        "padding": "0",
        "zIndex": "100",
        "boxShadow": "1px 0 0 #E5E7EB",
    }, children=[
        # Logo area
        html.Div(style={"padding": "24px 20px 20px", "borderBottom": f"1px solid {C_BORDER}"}, children=[
            html.Div(style={"display":"flex","alignItems":"center","gap":"10px"}, children=[
                html.Div("T", style={
                    "width":"34px","height":"34px","background":"linear-gradient(135deg,#E63946,#C1121F)",
                    "borderRadius":"8px","display":"flex","alignItems":"center","justifyContent":"center",
                    "color":"#fff","fontWeight":"700","fontSize":"16px","fontFamily":"DM Sans, sans-serif"
                }),
                html.Div([
                    html.Div("TSLA", style={"fontWeight":"700","fontSize":"15px","color":C_DARK,"lineHeight":"1.2","fontFamily":"DM Sans, sans-serif"}),
                    html.Div("Analytics", style={"fontWeight":"400","fontSize":"11px","color":C_GRAY,"fontFamily":"DM Sans, sans-serif"}),
                ])
            ])
        ]),
        # Nav
        html.Div(style={"padding":"12px 12px","flex":"1"}, children=[
            html.Div("NAVIGATION", style={"fontSize":"10px","fontWeight":"600","color":"#9CA3AF","letterSpacing":"0.1em","padding":"4px 8px","marginBottom":"4px"}),
            *[html.Div(
                id=f"nav-{tab_id}",
                n_clicks=0,
                style={
                    "padding":"10px 12px","marginBottom":"4px","borderRadius":"8px","cursor":"pointer",
                    "display":"flex","alignItems":"center","gap":"8px","transition":"all 0.2s ease",
                    "fontSize":"13px","fontWeight":"500","color":C_GRAY,"userSelect":"none"
                },
                children=[html.Span(icon, style={"fontSize":"16px"}), text],
                **{"data-tab": tab_id}
            ) for icon, text, tab_id in nav_items]
        ]),
        # Footer info
        html.Div(style={"padding":"12px 20px 20px","borderTop":f"1px solid {C_BORDER}","fontSize":"10px","color":C_GRAY"}, children=[
            html.Div("TSLA Analytics", style={"fontWeight":"600","marginBottom":"4px"}),
            html.Div("Powered by PostgreSQL", style={"opacity":"0.7"}),
        ])
    ])

def render_overview():
    if df.empty:
        return html.Div("No data available", style={"padding":"20px", "color": C_GRAY})
    
    latest = df.iloc[-1] if len(df) > 0 else {}
    prev = df.iloc[-2] if len(df) > 1 else {}
    
    change = (latest.get("Close", 0) - prev.get("Close", 0)) / prev.get("Close", 1) * 100 if prev.get("Close", 0) != 0 else 0
    
    return html.Div([
        card([
            section_label("Current Snapshot"),
            html.Div(style={"display":"grid","gridTemplateColumns":"repeat(auto-fit, minmax(200px, 1fr))","gap":"16px"}, children=[
                html.Div([
                    html.Div(f"${latest.get('Close', 'N/A'):.2f}", style={"fontSize":"28px","fontWeight":"700","color":C_DARK}),
                    html.Div("Current Price", style={"fontSize":"12px","color":C_GRAY}),
                    html.Div(f"{'+' if change > 0 else ''}{change:.2f}%", style={
                        "fontSize":"12px","fontWeight":"600","color":C_GREEN if change > 0 else C_RED,"marginTop":"4px"
                    })
                ]),
                html.Div([
                    html.Div(f"${latest.get('High', 'N/A'):.2f}", style={"fontSize":"20px","fontWeight":"600","color":C_DARK}),
                    html.Div("Daily High", style={"fontSize":"12px","color":C_GRAY}),
                ]),
                html.Div([
                    html.Div(f"${latest.get('Low', 'N/A'):.2f}", style={"fontSize":"20px","fontWeight":"600","color":C_DARK}),
                    html.Div("Daily Low", style={"fontSize":"12px","color":C_GRAY}),
                ]),
            ])
        ]),
    ])

def render_eda():
    if df.empty or df_2024.empty:
        return html.Div("No data available", style={"padding":"20px", "color": C_GRAY})
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_2024["Date"], y=df_2024["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color=C_RED, width=2),
        fill="tozeroy",
        fillcolor=C_RED_BG,
    ))
    fig.update_layout(chart_layout("Tesla Stock Price — 2024", 400))
    
    return html.Div([
        card([section_label("2024 Performance"), dcc.Graph(figure=fig, config={"responsive":True, "displayModeBar":False})])
    ])

def render_predictions():
    if not model_preds or len(model_preds.get("sarima", pd.DataFrame())) == 0:
        return html.Div("No predictions available", style={"padding":"20px", "color": C_GRAY})
    
    fig = make_subplots(rows=1, cols=1)
    
    sarima_df = model_preds.get("sarima", pd.DataFrame())
    prophet_df = model_preds.get("prophet", pd.DataFrame())
    
    if not sarima_df.empty:
        fig.add_trace(go.Scatter(
            x=sarima_df["Date"], y=sarima_df["Actual"],
            mode="lines",
            name="Actual",
            line=dict(color=C_DARK, width=2)
        ))
        fig.add_trace(go.Scatter(
            x=sarima_df["Date"], y=sarima_df["SARIMA_Pred"],
            mode="lines",
            name="SARIMA",
            line=dict(color=C_BLUE, width=2, dash="dash")
        ))
    
    if not prophet_df.empty:
        fig.add_trace(go.Scatter(
            x=prophet_df["Date"], y=prophet_df["Prophet_Pred"],
            mode="lines",
            name="Prophet",
            line=dict(color=C_GREEN, width=2, dash="dot")
        ))
    
    fig.update_layout(chart_layout("Model Predictions Comparison", 400))
    
    return html.Div([
        card([section_label("AI Predictions"), dcc.Graph(figure=fig, config={"responsive":True, "displayModeBar":False})])
    ])

def render_news():
    impact_colors = {"Positive": C_GREEN, "Negative": C_RED, "Neutral": C_AMBER}
    impact_bg     = {"Positive": C_GREEN_BG, "Negative": C_RED_BG, "Neutral": C_AMBER_BG}
    impact_icon   = {"Positive": "↑", "Negative": "↓", "Neutral": "→"}

    news_items = []
    for item in tesla_news:
        color  = impact_colors.get(item["impact"], C_GRAY)
        bg     = impact_bg.get(item["impact"], C_BG)
        icon   = impact_icon.get(item["impact"], "—")

        news_items.append(html.Div(className="news-card", style={
            "background":C_CARD,"borderRadius":"14px","padding":"22px 24px",
            "marginBottom":"14px",
            "boxShadow":"0 1px 3px rgba(0,0,0,0.05), 0 2px 8px rgba(0,0,0,0.04)",
            "border":f"1px solid {C_BORDER}",
            "borderLeft":f"4px solid {color}",
            "transition":"all 0.2s ease","cursor":"default",
        }, children=[
            html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center","marginBottom":"12px"}, children=[
                html.Div(style={"display":"flex","alignItems":"center","gap":"10px"}, children=[
                    html.Div(item["source_icon"], style={"fontSize":"18px"}),
                    html.Div([
                        html.Span(item["source"], style={"fontSize":"13px","fontWeight":"600","color":C_DARK}),
                        html.Span(" · ", style={"color":C_BORDER}),
                        html.Span(item["date"], style={"fontSize":"12px","color":C_GRAY}),
                    ])
                ]),
                html.Div(style={"display":"flex","gap":"8px","alignItems":"center"}, children=[
                    html.Div(item["tag"], style={
                        "fontSize":"11px","fontWeight":"600","padding":"3px 10px",
                        "borderRadius":"20px","background":C_BG,"color":C_GRAY,
                        "border":f"1px solid {C_BORDER}"
                    }),
                    html.Div(
                        f"{icon} {item['impact']}",
                        style={
                            "fontSize":"11px","fontWeight":"700","padding":"3px 10px",
                            "borderRadius":"20px","background":bg,"color":color,
                        }
                    ),
                ])
            ]),
            html.H4(item["headline"], style={
                "margin":"0 0 8px","fontSize":"15px","fontWeight":"600",
                "color":C_DARK,"lineHeight":"1.4"
            }),
            html.P(item["summary"], style={
                "margin":"0 0 14px","fontSize":"13px","color":C_GRAY,
                "lineHeight":"1.6"
            }),
            html.Div(style={"display":"flex","alignItems":"center","gap":"12px"}, children=[
                html.A("Read Article →", href=item["url"], target="_blank", rel="noopener noreferrer", style={
                    "fontSize":"12px","fontWeight":"600","color":color,
                    "textDecoration":"none","padding":"6px 14px",
                    "border":f"1px solid {color}","borderRadius":"6px",
                    "background":bg,
                }),
            ])
        ]))

    pos = sum(1 for n in tesla_news if n["impact"] == "Positive")
    neg = sum(1 for n in tesla_news if n["impact"] == "Negative")
    neu = sum(1 for n in tesla_news if n["impact"] == "Neutral")
    total = len(tesla_news)

    sentiment_bar = card([
        section_label("Sentiment Overview"),
        html.Div(style={"display":"flex","gap":"20px","marginBottom":"16px"}, children=[
            html.Div([
                html.Div(f"{pos}", style={"fontSize":"28px","fontWeight":"700","color":C_GREEN}),
                html.Div("Positive", style={"fontSize":"12px","color":C_GRAY}),
            ]),
            html.Div([
                html.Div(f"{neg}", style={"fontSize":"28px","fontWeight":"700","color":C_RED}),
                html.Div("Negative", style={"fontSize":"12px","color":C_GRAY}),
            ]),
            html.Div([
                html.Div(f"{neu}", style={"fontSize":"28px","fontWeight":"700","color":C_AMBER}),
                html.Div("Neutral", style={"fontSize":"12px","color":C_GRAY}),
            ]),
        ]),
        html.Div(style={"display":"flex","borderRadius":"6px","overflow":"hidden","height":"8px"}, children=[
            html.Div(style={"flex":str(pos),"background":C_GREEN}),
            html.Div(style={"flex":str(neg),"background":C_RED}),
            html.Div(style={"flex":str(neu),"background":C_AMBER}) if neu else html.Div(),
        ]),
        html.Div(f"Based on {total} curated news items — Q4 2023 through Q1 2024",
                 style={"fontSize":"11px","color":C_GRAY,"marginTop":"10px"}),
    ])

    return html.Div([
        sentiment_bar,
        card([
            section_label("Latest TSLA News"),
            html.Div(news_items)
        ])
    ])

# Main layout
app.layout = html.Div(style={"display":"flex","minHeight":"100vh"}, children=[
    sidebar(),
    html.Div(id="main-content", style={
        "flex":"1","overflowY":"auto","padding":"40px","background":C_BG,
    }, children=[
        html.Div(id="page-title", style={"fontSize":"32px","fontWeight":"700","color":C_DARK,"marginBottom":"4px"}),
        html.Div(id="page-subtitle", style={"fontSize":"14px","color":C_GRAY,"marginBottom":"32px"}),
        html.Div(id="page-content"),
    ]),
    dcc.Store(id="current-tab", data="overview")
])

# Callbacks
@app.callback(
    [Output("main-content", "children"), Output("current-tab", "data")],
    [Input(f"nav-{tab_id}", "n_clicks") for tab_id, _, _ in [("overview", "", ""), ("eda", "", ""), ("predictions", "", ""), ("news", "", "")]],
    prevent_initial_call=False
)
def update_page(*clicks):
    # Simplified - just rotate through pages
    return [
        html.Div(id="page-title", children="Overview", style={"fontSize":"32px","fontWeight":"700","color":C_DARK,"marginBottom":"4px"}),
        html.Div(id="page-subtitle", children="Current Market Snapshot", style={"fontSize":"14px","color":C_GRAY,"marginBottom":"32px"}),
        render_overview()
    ], "overview"

if __name__ == "__main__":
    app.run(debug=False, port=8050, host="0.0.0.0")
