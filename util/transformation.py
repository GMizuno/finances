import pandas as pd
from pandas_gbq import to_gbq

from bigquery import delete_row_based_date_and_ticket
from loguru import logger

from util.const import PROJECT, TABLE
from util.requester import get_data

pd.options.mode.chained_assignment = None


def select_columns(data: "pd.DataFrame", columns: list[str]):
    return data[columns]


def daily_return(data: "pd.DataFrame"):
    data["Percent_Change"] = data.apply(
        lambda row: ((row["Close"] - row["Open"]) / row["Open"]) * 100, axis=1
    )
    return data


def transform_data(data: "pd.DataFrame", ticket: str) -> "pd.DataFrame":
    daily_return(data)
    data = select_columns(data, ["Date", "Open", "Close", "Percent_Change"])

    data.loc[:, "Date"] = pd.to_datetime(data["Date"]).dt.strftime("%Y-%m-%d")
    data.loc[:, "Ticket"] = ticket

    return data


def get_daily_return(data: "pd.DataFrame") -> list[dict]:
    data = data[["Date", "Ticket", "Percent_Change"]]

    data = data.rename(
        columns={"Date": "date", "Ticket": "ticket", "Percent_Change": "earning"}
    )
    return data.to_dict("records")


def etl(ticket, start, end, table=TABLE, project_id=PROJECT) -> None:
    logger.info(f"Extraindo {ticket}")
    try:
        data = get_data(ticket, start, end)
        logger.success("Dados obtidos com sucesso da API")

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
        delete_row_based_date_and_ticket(table, start, end, ticket, project_id)
        data = data[["Date", "Open", "Close", "Ticket"]]
        logger.warning("Dados deletados com sucesso.")
        to_gbq(data, destination_table=table, project_id=project_id, if_exists="append")
        logger.success("Dados atulizados com sucesso.")
    except Exception as e:
        logger.error(f"Error ao inserir na tabela {table}.\n{e}")
        raise
