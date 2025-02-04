import functions_framework
import yfinance as yf
import pendulum
import pandas as pd
from pandas_gbq import to_gbq, read_gbq

from discord import parser_fail_msg, parser_sucess_msg, send_discord

TABLE = "finances.finance_raw"
PROJECT = "cartola-360814"

def get_data(ticket: str, start: str, end: str) -> 'pd.DataFrame':
    return yf.Ticker(ticket).history(start=start, end=end).reset_index()

def select_columns(data: 'pd.DataFrame', columns: list[str]):
    return data[columns]

def transform_data(data: 'pd.DataFrame', ticket: str) -> 'pd.DataFrame':
    data = select_columns(data, ['Date', 'Open', 'Close'])
    data.loc[:, 'Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')

    data.loc[:, 'Ticket'] = ticket
    return data

def delete_row_based_date_and_ticket(table: str, start_date: str, end_date: str, ticket:str, project: str = PROJECT):
    query = f"""
    DELETE
    FROM `{table}`
    WHERE `Date` BETWEEN "{start_date}" AND "{end_date}" AND Ticket = "{ticket}"
    """
    print(f'Running query {query}')
    read_gbq(query, project_id=project)

@functions_framework.http
def main(request):
    request_json = request.get_json(silent=True)
    tickets = request_json.get('tickets')
    start = request_json.get('start')
    end = request_json.get('end')

    print(f'Extraindo dados dos seguintes ativos {tickets}')

    if start is None:
        start = pendulum.today().subtract(days=1).to_date_string()
        end = pendulum.tomorrow().to_date_string()

    for ticket in tickets:
        print(f'Extraindo {ticket}')
        try:
            print(f'Extracting data from {start} to {end}')
            data = get_data(ticket, start, end)
        except Exception as e:
            raise ValueError(f"Error ao extrair dados.\n{e}")

        try:
            data = transform_data(data, ticket)
        except Exception as e:
            raise ValueError(f"Error ao tratar dados.\n{e}")

        try:
            delete_row_based_date_and_ticket(TABLE, start, end, ticket)
            to_gbq(
                data,
                destination_table=TABLE,
                project_id=PROJECT,
                if_exists="append"
            )
        except Exception as e:
            msg = parser_fail_msg(str(e), ticket)
            send_discord(msg)
            raise ValueError(f'Erro ao inserir na tabela {TABLE}.\n{e}')

    msg = parser_sucess_msg(tickets, start, end)
    send_discord(msg)
    return ""

# if __name__ == "__main__":
#     from mock import mock_request
#     main(mock_request)
#
