import yfinance as yf
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

def get_data(ticket: str, start: str, end: str) -> "pd.DataFrame":
    return yf.Ticker(ticket).history(start=start, end=end).reset_index()


x = get_data("B5P211.SA", '2025-02-19', '2025-02-21')
