import yfinance as yf


def get_data(ticket: str, start: str, end: str) -> "pd.DataFrame":
    if start is None and end is None:
        return yf.Ticker(ticket).history(period="2mo").reset_index()
    return yf.Ticker(ticket).history(start=start, end=end).reset_index()


x = get_data("B5P211.SA", None, None)
