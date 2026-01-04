import os
import sys
import json

from dotenv import load_dotenv
from src.util.log import logger, metrics
from src.util.secret import get_secret
from src.util.bigquery import get_bigquery_client, truncate_and_insert
from src.util.requester import get_data
from src.message.discord import send_discord, parser_sucess_msg
from src.util.send_mom_return import QUERY_MONTHLY_RETURN, TICKETS_MONTHLY_RETURN, render_mom_return_template
import pendulum
import awswrangler as wr

load_dotenv()

wr.config.s3_output = "s3://aws-athena-query-results-605771322130-us-east-2/"


def main(event, context) -> dict:
    logger.info(f"Starting the process with event {event} and context {context}")

    tickets = os.getenv("TICKETS").split(",")
    start = os.getenv("START", None)
    end = os.getenv("END", None)
    webhook = json.loads(get_secret("msg/discord"))["webhook"]
    metrics.add_dimension(name="data_type", value=data_type)

    if start is not None and end is not None:
        logger.info(f"Using custom range {start} to {end}")
        start = pendulum.today().subtract(days=30).to_date_string()
        end = pendulum.today().subtract(days=0).to_date_string()

    logger.info(f"Extracting these {tickets} from range {start} to {end}")

    for ticket in tickets:
        logger.info(f"Starting processing {ticket}")
        metrics.add_dimension(name="ticket", value=ticket)

        data = get_data(ticket, start, end)

        metrics.add_metric(name="ProcessedRecords", unit="Count", value=len(data))
        metrics.add_metric(name="ProcessedColumns", unit="Count", value=len(data.columns))

        logger.success("Extract from Yahoo Finance")

        data["Date"] = data["Date"].dt.tz_convert("UTC").dt.tz_localize(None)
        data.rename(columns={"Stock Splits": "Stock_Splits"}, inplace=True)

        logger.success("Cleaning columns")

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
            metrics.add_metric(name="ErrorCount", unit="Count", value=1)
            continue

        data = data[required_columns]
        data["Ticket"] = ticket
        try:
            logger.info(f"Writing to Athena table {ticket}")

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
            metrics.add_metric(name="ErrorCount", unit="Count", value=1)
            sys.exit(1)

        try:
            logger.info(f"Writing to BigQuery table {ticket}")
            biqquey_client = get_bigquery_client()
            data_bigquery = data[["Date", "Open", "Close", "Ticket"]]
            truncate_and_insert(biqquey_client, ticket, data_bigquery, "finances", "finance_raw")
            logger.success(f"Finished sending {ticket} to BigQuery")
        except Exception as e:
            logger.error(f"BigQuery write error for ticket {ticket}: {e}")
            metrics.add_metric(name="ErrorCount", unit="Count", value=1)
            sys.exit(1)

    try:
        logger.info("Sending Discord msg")
        start = data["Date"].min().date()
        end = data["Date"].max().date()
        send_discord(parser_sucess_msg(tickets, start, end), webhook)

        logger.info("Sending Monthly return msg")

        monthly_return_msg = render_mom_return_template(QUERY_MONTHLY_RETURN, TICKETS_MONTHLY_RETURN)
        send_discord(monthly_return_msg, webhook)
    except Exception as e:
        metrics.add_metric(name="ErrorCount", unit="Count", value=1)
        logger.error(f"Error on send Discord msg {tickets}: {e}")

    logger.success("Finished processing all tickets.")
    metrics.add_metric(name="SucessCount", unit="Count", value=1)
    return {"statusCode": 200, "body": json.dumps("Finished processing all tickets.")}
