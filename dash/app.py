import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime
from PricingLib.QuOPERA import Surface
from Scrapers.YahooScraping import update

app = dash.Dash(__name__)

c_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Calls_AAPL_Last.csv')
p_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Puts_AAPL_Last.csv')
surf=Surface()
surf.load_last_data()


app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div(html.H1('OPERA Dashboard'), className="app-header--title")
        ]
    ),
    html.H2("Vol K T visualization"),
    html.P("Zone test"),
    html.Div(className="parent",children=[
        html.Div(id="left",children=[html.Button('Refresh data', id='refresh-data')]),
        html.Div(id="right",children=[html.P(id='update-date',children="No updates in current session, please update")])
    ]
    ),
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
    ),dcc.Graph(
        id="vol", config={"displayModeBar": False},
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
                "text": f"Call prices of {ticker} on {date} wrt strike",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return x


@app.callback(
    Output("vol","figure"),
    [
        Input("dates","value"),
        Input("ticker","value")
    ],
)
def update_vol(date,ticker):
    mask = (set(c_data["Date"]) == date)
    vols=surf.C_imp_vol[mask]
    mask2 = (c_data["Date"] == date)
    filtered = c_data.loc[mask2, :]
    x={
        "data": [
            {
                "x": filtered["Strike"],
                "y": vols,
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"Call implied volatilities of {ticker} on {date} wrt strike",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "%", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return x

@app.callback(Output("update-date", "children"),
    Input('refresh-data', 'value')
)
def update_data(value):
    update()
    global c_data
    global p_data
    global surf

    c_data= pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Calls_AAPL_Last.csv')
    p_data= pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Puts_AAPL_Last.csv')
    surf = Surface()
    surf.load_last_data()
    dte=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Last update : {dte}"


if __name__ == '__main__':
    app.run_server(debug=True)