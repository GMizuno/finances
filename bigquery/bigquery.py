import pandas as pd


def select_columns(data: 'pd.DataFrame', columns: list[str]):
    return data[columns]


def transform_data(data: 'pd.DataFrame', ticket: str) -> 'pd.DataFrame':
    data = select_columns(data, ['Date', 'Open', 'Close'])
    data.loc[:, 'Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')

    data.loc[:, 'Ticket'] = ticket
    return data
