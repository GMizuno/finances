from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

def daily_return(data: pd.DataFrame):
    data['Percent_Change'] = data.apply(lambda row: ((row['Close'] - row['Open']) / row['Open']) * 100, axis=1)
    return data