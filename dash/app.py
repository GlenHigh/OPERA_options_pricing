import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        options=[
            {'label': 'Apple AAPL', 'value': 'AAPL'},
            {'label': 'Microsoft MSFT', 'value': 'MTL'},
            {'label': 'CAC40 FCHI', 'value': '^FCHI'}
        ],
        value='AAPL'
    )
])

c_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Calls_AAPL_Last.csv')
p_data = pd.read_csv('/Users/glenhigh/Scrapping/OPERA_options_pricing/Market_data/Puts_AAPL_Last.csv')


if __name__ == '__main__':
    app.run_server(debug=True)