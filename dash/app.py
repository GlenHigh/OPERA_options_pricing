import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__)

c_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Calls_AAPL_Last.csv')
p_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Puts_AAPL_Last.csv')



app.layout = html.Div([
    html.H1("Vol K T visualization"),
    html.P("Zone test"),
    dcc.Dropdown(
        id="ticker",
        options=[
            {'label': 'Apple AAPL', 'value': 'AAPL'},
            {'label': 'Microsoft MSFT', 'value': 'MTL'},
            {'label': 'CAC40 FCHI', 'value': '^FCHI'}
        ],
        value='AAPL'
    ),
    dcc.Dropdown(
        id="dates",
        options=[
            {'label':date, 'value':date}
            for date in set(c_data['Date'])
        ],
        value=c_data['Date'][0]
    ),
    dcc.Graph(
        id="price", config={"displayModeBar": False},
    )
])

@app.callback(
    Output("price","figure"),
    [
        Input("dates","value"),
        Input("ticker","value")
    ],
)
def update_price(date,ticker):
    mask = (c_data["Date"] == date)
    filtered=c_data.loc[mask,:]
    x={
        "data": [
            {
                "x": filtered["Strike"],
                "y": filtered["Last Price"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"Price of {ticker} on {date}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return x

if __name__ == '__main__':
    app.run_server(debug=True)