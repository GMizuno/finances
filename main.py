import functions_framework
import pendulum
from pandas_gbq import to_gbq

from bigquery.bigquery import delete_row_based_date_and_ticket
from util.transformation import transform_data
from message.discord import parser_fail_msg, parser_sucess_msg, send_discord
from util.requester import get_data

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
            # TODO - Criar estrutura de msg
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
    send_discord(msg)
    return ""

# if __name__ == "__main__":
#     from mock import mock_request
#     main(mock_request)

