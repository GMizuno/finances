import pendulum
import awswrangler as wr
import os
from dotenv import load_dotenv
import json
import sys

from src.message.discord import parser_sucess_msg, send_discord
from src.util.requester import get_data
from src.util.log import logger
from src.util.secret import get_secret

load_dotenv()


def main(event, context) -> dict:
    logger.info(f"Starting the process with event {event} and context {context}")

    tickets = os.getenv("TICKETS").split(",")
    start = os.getenv("START", None)
    end = os.getenv("END", None)
    webhook = json.loads(get_secret('msg/discord'))['webhook']

    if start is not None and end is not None:
        logger.info(f"Using custom range {start} to {end}")
        start = pendulum.today().subtract(days=30).to_date_string()
        end = pendulum.today().subtract(days=0).to_date_string()

    logger.info(f"Extracting these {tickets} from range {start} to {end}")

    for ticket in tickets:
        logger.info(f"Starting processing {ticket}")

        data = get_data(ticket, start, end)

        logger.success(f"Extract from Yahoo Finance")

        data["Date"] = data["Date"].dt.tz_convert("UTC").dt.tz_localize(None)
        data.rename(columns={"Stock Splits": "Stock_Splits"}, inplace=True)

        logger.success(f"Cleaning columns")

        # TODO: MOVE AS CONST
        required_columns = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Dividends",
        ]
        missing_columns = [col for col in required_columns if col not in data.columns]

        logger.info(f"Selected columns: {required_columns}")
        if missing_columns:
            logger.error(f"Missing columns for ticket {ticket}: {missing_columns}")
            continue

        data = data[required_columns]
        data["Ticket"] = ticket
        try:
            logger.info(f"Writing to Athena table {ticket}")

            # TODO: PASS AS PARAMETRE
            wr.config.s3_output = "s3://aws-athena-query-results-605771322130-us-east-2/"

            wr.athena.to_iceberg(
                df=data,
                database="corretagem",
                table="stock_data",
                temp_path="s3://finance-605771322130/temp/",
                table_location="s3://finance-605771322130/raw/stock_data/",
                keep_files=False,
            )
            logger.success(f"Finished processing {ticket}")
        except Exception as e:
            logger.error(f"Athena write error for ticket {ticket}: {e}")
            sys.exit(1)

    try:
        send_discord(parser_sucess_msg(tickets, start, end), webhook)
    except Exception as e:
        logger.error(f"Error on send Discord msg {tickets}: {e}")

    logger.success("Finished processing all tickets.")
    return {
        'statusCode': 200,
        'body': json.dumps("Finished processing all tickets.")
    }
