import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request
from volatility import calculate_volatility, plot_two_portfolios_with_regression, create_table
import matplotlib
matplotlib.use('Agg')  # Use a backend that doesn't require a display

app = Flask(__name__)

# Function to validate the ticker
def is_valid_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # Check for the presence of a key that indicates a valid ticker
        return info and 'shortName' in info and info['shortName'] is not None
    except Exception as e:
        print(f"Error validating ticker {ticker}: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    tickers_list = request.form.getlist('tickers')
    prices_list = request.form.getlist('prices')

    # Validate the tickers and clean the data
    tickers_list = [ticker.strip().upper() for ticker in tickers_list]
    valid_tickers = [ticker for ticker in tickers_list if is_valid_ticker(ticker)]
    
    prices_list = [float(price.strip()) for price in prices_list]
        
    table = create_table(valid_tickers)
    
    print(table)
        
    all_closings = pd.read_csv('closingPrices.csv')
    ticker_list = table['Ticker'].tolist()
    suggested_ticker_list = table['Suggested Ticker'].tolist()
    
    print(ticker_list)
    print(suggested_ticker_list)

    plot_two_portfolios_with_regression(ticker_list,suggested_ticker_list,prices_list, all_closings )


    return render_template('results.html', tables=table.to_html(classes='data-table', index=False))

if __name__ == '__main__':
    app.run(debug=True)
