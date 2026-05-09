"""Main Dash application untuk TSLA Analytics Dashboard"""
import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging
from datetime import datetime
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from database import init_pool, close_all_connections
    from data_accessor import DataAccessor
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    raise

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database pool
try:
    init_pool()
    logger.info("Database pool initialized for Dash app")
    DB_AVAILABLE = True
except Exception as e:
    logger.warning(f"Database not available on startup (will retry on first request): {e}")
    DB_AVAILABLE = False

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # For Vercel deployment

# CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>TSLA Analytics Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                padding: 30px;
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                font-size: 0.9em;
                margin-bottom: 30px;
            }
            .metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .metric-value {
                font-size: 1.8em;
                font-weight: bold;
                margin: 10px 0;
            }
            .metric-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
            .tabs {
                margin-top: 30px;
            }
            .graph-container {
                margin: 20px 0;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
            }
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

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("📈 TSLA Analytics Dashboard"),
        html.Div("Tesla Stock Price Analysis & Predictions", className="subtitle"),
        
        # Metrics row
        html.Div(id='metrics-container', className='metrics'),
        
        # Tabs
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='📊 Stock Price Analysis', value='tab-1', children=[
                html.Div([
                    dcc.Loading(
                        id="loading-stock",
                        type="default",
                        children=[dcc.Graph(id='stock-graph', style={'height': '500px'})]
                    )
                ], className='graph-container')
            ]),
            
            dcc.Tab(label='🔮 Predictions', value='tab-2', children=[
                html.Div([
                    dcc.Loading(
                        id="loading-predictions",
                        type="default",
                        children=[dcc.Graph(id='predictions-graph', style={'height': '500px'})]
                    )
                ], className='graph-container')
            ]),
            
            dcc.Tab(label='📋 Model Performance', value='tab-3', children=[
                html.Div([
                    dcc.Loading(
                        id="loading-evaluation",
                        type="default",
                        children=[html.Div(id='evaluation-table')]
                    )
                ], className='graph-container')
            ]),
            
            dcc.Tab(label='ℹ️ API Info', value='tab-4', children=[
                html.Div([
                    html.H3("Available API Endpoints"),
                    html.Pre(id='api-info', style={
                        'background': '#f0f0f0',
                        'padding': '20px',
                        'border-radius': '8px',
                        'overflow': 'auto'
                    })
                ], className='graph-container')
            ]),
        ]),
        
    ], className='container'),
    
    # Interval for auto-refresh
    dcc.Interval(id='interval-component', interval=300000, n_intervals=0),
])

# Callbacks
@callback(
    Output('metrics-container', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    """Update metrics"""
    try:
        if not DB_AVAILABLE:
            try:
                init_pool()
            except:
                pass
        
        df = DataAccessor.get_tesla_stock_data()
        latest = df.iloc[-1] if len(df) > 0 else None
        
        if latest is not None:
            current_price = latest['close']
            prev_close = df.iloc[-2]['close'] if len(df) > 1 else current_price
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close != 0 else 0
            
            change_color = "#00c853" if change >= 0 else "#d32f2f"
            change_arrow = "📈" if change >= 0 else "📉"
            
            return [
                html.Div([
                    html.Div("Current Price", className='metric-label'),
                    html.Div(f"${current_price:.2f}", className='metric-value'),
                ], className='metric-card'),
                
                html.Div([
                    html.Div("24h Change", className='metric-label'),
                    html.Div(f"{change_arrow} {change_pct:.2f}%", className='metric-value'),
                ], className='metric-card', style={'background': f'linear-gradient(135deg, {change_color} 0%, {change_color}88 100%)'}),
                
                html.Div([
                    html.Div("High (Today)", className='metric-label'),
                    html.Div(f"${latest['high']:.2f}", className='metric-value'),
                ], className='metric-card'),
                
                html.Div([
                    html.Div("Low (Today)", className='metric-label'),
                    html.Div(f"${latest['low']:.2f}", className='metric-value'),
                ], className='metric-card'),
            ]
        else:
            return html.Div("Loading data...", style={'color': '#999', 'padding': '20px'})
    except Exception as e:
        logger.warning(f"Error updating metrics: {e}")
        return html.Div([
            html.Div([
                html.Div("Status", className='metric-label'),
                html.Div("Loading...", className='metric-value'),
            ], className='metric-card'),
            html.Div([
                html.Div("Note", className='metric-label'),
                html.Div("Connecting to database", className='metric-value'),
            ], className='metric-card'),
        ])

@callback(
    Output('stock-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_stock_graph(n):
    """Update stock price graph"""
    try:
        df = DataAccessor.get_tesla_stock_data()
        
        # Get last 3 months
        df_recent = df.tail(90)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_recent['date'],
            y=df_recent['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#667eea', width=2),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig.update_layout(
            title='Tesla Stock Price (Last 3 Months)',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        return fig
    except Exception as e:
        logger.error(f"Error updating stock graph: {e}")
        return go.Figure().add_annotation(text=f"Error loading data: {str(e)}")

@callback(
    Output('predictions-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_predictions_graph(n):
    """Update predictions graph"""
    try:
        sarima_df = DataAccessor.get_sarima_predictions()
        prophet_df = DataAccessor.get_prophet_predictions()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=sarima_df['date'],
            y=sarima_df['predicted_price'],
            mode='lines',
            name='SARIMA',
            line=dict(color='#667eea', width=2, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=prophet_df['date'],
            y=prophet_df['predicted_price'],
            mode='lines',
            name='Prophet',
            line=dict(color='#764ba2', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Price Predictions Comparison',
            xaxis_title='Date',
            yaxis_title='Predicted Price ($)',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        return fig
    except Exception as e:
        logger.error(f"Error updating predictions graph: {e}")
        return go.Figure().add_annotation(text=f"Error loading predictions: {str(e)}")

@callback(
    Output('evaluation-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_evaluation_table(n):
    """Update model evaluation table"""
    try:
        df = DataAccessor.get_model_evaluation()
        
        # Create HTML table
        table = html.Table([
            html.Thead(
                html.Tr([
                    html.Th(col, style={'padding': '10px', 'text-align': 'left', 'border-bottom': '2px solid #667eea'})
                    for col in df.columns
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(str(row[col]), style={'padding': '10px', 'border-bottom': '1px solid #ddd'})
                    for col in df.columns
                ])
                for idx, row in df.iterrows()
            ])
        ], style={'width': '100%', 'border-collapse': 'collapse'})
        
        return table
    except Exception as e:
        logger.error(f"Error updating evaluation: {e}")
        return html.Div(f"Error loading evaluation: {str(e)}", style={'color': 'red'})

@callback(
    Output('api-info', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_api_info(n):
    """Update API info"""
    api_endpoints = """
AVAILABLE ENDPOINTS:

📊 Stock Data:
  GET /api/stock/all                    - Get all stock data
  GET /api/stock/latest                 - Get latest stock price
  GET /api/stock/year/<year>            - Get data for specific year
  GET /api/stock/year/<year>/quarter/<q> - Get data for specific quarter

🔮 Predictions:
  GET /api/predictions/sarima           - SARIMA model predictions
  GET /api/predictions/prophet          - Prophet model predictions
  GET /api/predictions/combined         - Combined predictions

📋 Models:
  GET /api/models/evaluation            - Model performance metrics

✅ Health:
  GET /api/health                       - Health check

📚 Documentation:
  GET /                                 - API documentation
  GET /api                              - API info
"""
    return api_endpoints

# For Vercel deployment
def handler(request):
    """Vercel handler"""
    return app.server(request.environ, request.start_response)

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=3000)
