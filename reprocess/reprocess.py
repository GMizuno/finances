import pendulum
from pandas_gbq import to_gbq

from bigquery import delete_row_based_date_and_ticket
from util.const import PROJECT, SELECT_TICKET, TABLE
from util.log import logger
from util.requester import get_data
from util.transformation import transform_data


def reprocess_data(tickets, start, end):
    if start is None:
        start = pendulum.today().subtract(days=1).to_date_string()
        end = pendulum.tomorrow().to_date_string()

    for ticket in tickets:
        logger.info(f"Extraindo {ticket}")
        try:
            logger.info(f"Extracting data from {start} to {end}")
            data = get_data(ticket, start, end)
            logger.success('Dados obtidos com sucesso da API')

        except Exception as e:
            logger.error(f"Error ao extrair dados.\n{e}")
            raise 

        try:
            data = transform_data(data, ticket)
            logger.success("Dados tratados com sucesso.")
        except Exception as e:
            logger.error(f"Error ao tratar dados.\n{e}")
            raise

        try:
            delete_row_based_date_and_ticket(TABLE, start, end, ticket, PROJECT)
            logger.warning("Dados deletados com sucesso.")
            data = data[["Date", "Open", "Close", "Ticket"]]
            to_gbq(
                data, destination_table=TABLE, project_id=PROJECT, if_exists="append"
            )
            logger.success("Dados atulizados com sucesso.")
        except Exception as e:
            logger.error(f"Error ao inserir na tabela {TABLE}.\n{e}")
            raise


if __name__ == "__main__":
    start = "2024-01-01"
    end = "2025-12-31"
    reprocess_data(SELECT_TICKET, start, end)
