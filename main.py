import functions_framework
import pendulum
from pandas_gbq import to_gbq

from bigquery import delete_row_based_date_and_ticket
from bigquery.bigquery import run_query
from message.render_jinja import month_over_month
from message.discord import parser_fail_msg, parser_sucess_msg, send_discord
from util.requester import get_data
from util.transformation import transform_data

TABLE = "finances.finance_raw"
PROJECT = "cartola-360814"


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
            delete_row_based_date_and_ticket(TABLE, start, end, ticket, PROJECT)
            data = data[['Date', 'Open', 'Close', 'Ticket']]
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

    query = '''
            SELECT year_month, DATE, Ticket, return_pct * 100 AS return_pct
            FROM `cartola-360814.finances.vw_return_mensal`
                QUALIFY ROW_NUMBER() OVER(PARTITION BY Ticket ORDER BY DATE DESC) < 2
            ORDER BY Ticket
            '''
    
    data_month_over_month =  run_query(query, PROJECT)
    data_month_over_month = data_month_over_month[data_month_over_month["Ticket"].isin(tickets)]

    msg = parser_sucess_msg(tickets, start, end)
    msg_month_over_month = month_over_month(data_month_over_month.to_dict(orient='records'))

    send_discord(msg)
    print('Sending message with month over the month returns')
    send_discord(msg_month_over_month)
    
    return ""
#
# if __name__ == "__main__":
#     from mock import mock_request
#     main(mock_request)
#
