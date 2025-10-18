TABLE = "finances.finance_raw"
PROJECT = "cartola-360814"
SELECT_TICKET = [
    "B5P211.SA",
    "SPXB11.SA",
    "IB5M11.SA",
    "NCIQ",
    "BIL",
]
QUERY = """
        SELECT year_month, DATE, Ticket, return_pct * 100 AS return_pct
        FROM `cartola-360814.finances.vw_return_mensal`
            QUALIFY ROW_NUMBER() OVER(PARTITION BY Ticket ORDER BY DATE DESC) < 2
        ORDER BY Ticket
        """
MIN_DATE = "2024-01-01"
MAX_DATE = "2025-12-31"
