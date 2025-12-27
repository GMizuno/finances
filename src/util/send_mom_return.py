import awswrangler as wr

from src.message.render_jinja import jinja_render

QUERY_MONTHLY_RETURN = """SELECT
        Ticket,
        max(operation_date) AS last_operation_date,
        max_by(close_price, operation_date) AS close_price,
        100*max_by(return_pct, operation_date) AS return_pct
    FROM corretagem.vw_month_return_asset
    WHERE Ticket IN ({tickets})
    GROUP BY Ticket
    """
TICKETS_MONTHLY_RETURN = "'B5P211.SA','SPXB11.SA','IB5M11.SA','BRL=X'"

def render_mom_return_template(query: str, tickets: str) -> str:

    query = query.format(tickets=tickets)
    df = wr.athena.read_sql_query(query, database="corretagem").to_dict("records")

    return jinja_render(df, template="mom.jinja")