import yfinance as yf

def get_info(ticker='CSU.TO'):
    
    stock = yf.Ticker(ticker)
    
    return float(stock.info['trailingAnnualDividendYield'])*100
