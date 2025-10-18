import pandas as pd

pd.options.mode.chained_assignment = None 

def select_columns(data: 'pd.DataFrame', columns: list[str]):
    return data[columns]


def daily_return(data: "pd.DataFrame"):
    data['Percent_Change'] = data.apply(lambda row: ((row['Close'] - row['Open']) / row['Open']) * 100, axis=1)
    return data


def transform_data(data: 'pd.DataFrame', ticket: str) -> 'pd.DataFrame':
    daily_return(data)
    data = select_columns(data, ['Date', 'Open', 'Close', 'Percent_Change'])

    data.loc[:, 'Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    data.loc[:, 'Ticket'] = ticket

    return data

def get_daily_return(data: 'pd.DataFrame') -> list[dict]:
    data = data[['Date', 'Ticket', 'Percent_Change']]
    
    data =  data.rename(columns={"Date": "date", "Ticket": "ticket", "Percent_Change": "earning"})
    return data.to_dict('records')




