import yfinance as yf

def get_data(ticket: str, start: str, end: str) -> "pd.DataFrame":
    return yf.Ticker(ticket).history(start=start, end=end).reset_index()

