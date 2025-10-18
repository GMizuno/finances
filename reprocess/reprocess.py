import pendulum

from util.const import SELECT_TICKET, TABLE
from loguru import logger
from util.transformation import etl


def reprocess_data(tickets, start, end):
    if start is None:
        start = pendulum.today().subtract(days=1).to_date_string()
        end = pendulum.tomorrow().to_date_string()

    logger.info(f"Extracting data from {start} to {end}")
    
    for ticket in tickets:
        try:
            etl(ticket, start, end)
        except Exception as e:
            logger.error(f"Error ao inserir na tabela {TABLE}.\n{e}")


if __name__ == "__main__":
    start = "2024-01-01"
    end = "2025-12-31"
    reprocess_data(SELECT_TICKET, start, end)
