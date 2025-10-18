from loguru import logger

import functions_framework
import pendulum

from bigquery.bigquery import run_query
from message.discord import parser_fail_msg, parser_sucess_msg, send_discord
from message.render_jinja import month_over_month
from util.const import PROJECT, QUERY, SELECT_TICKET, TABLE
from util.transformation import etl


@functions_framework.http
def main(request):
    request_json = request.get_json(silent=True)
    tickets = request_json.get("tickets")
    start = request_json.get("start")
    end = request_json.get("end")

    logger.info(f"Extraindo dados dos seguintes ativos {tickets}")

    if start is None:
        start = pendulum.today().subtract(days=1).to_date_string()
        end = pendulum.tomorrow().to_date_string()

    for ticket in tickets:
        try:
            etl(ticket, start, end)
        except Exception as e:
            msg = parser_fail_msg(str(e), ticket)
            send_discord(msg)
            logger.error(f"Error ao inserir na tabela {TABLE}.\n{e}")

    data_month_over_month = run_query(QUERY, PROJECT)
    data_month_over_month = data_month_over_month[
        data_month_over_month["Ticket"].isin(SELECT_TICKET)
    ]

    msg = parser_sucess_msg(tickets, start, end)
    msg_month_over_month = month_over_month(
        data_month_over_month.to_dict(orient="records")
    )

    send_discord(msg)
    logger.info("Sending message with month over the month returns")
    send_discord(msg_month_over_month)

    return ""
