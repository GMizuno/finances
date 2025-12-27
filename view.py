import awswrangler as wr

from src.message.render_jinja import jinja_render

query = """SELECT
    Ticket,
    max(operation_date) AS last_operation_date,
    max_by(close_price, operation_date) AS close_price,
    100*max_by(return_pct, operation_date) AS return_pct
FROM corretagem.vw_month_return_asset
WHERE Ticket IN ({tickets})
GROUP BY Ticket
"""

tickets = "'B5P211.SA','SPXB11.SA','IB5M11.SA','BRL=X'"
query = query.format(tickets=tickets)
df = wr.athena.read_sql_query(query, database="corretagem").to_dict("records")

render = jinja_render(df, template = "mom.jinja")