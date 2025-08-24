import yfinance as yf
from typing import TYPE_CHECKING


def get_data(ticket: str, start: str, end: str) -> "pd.DataFrame":
    return yf.Ticker(ticket).history(start=start, end=end).reset_index()

