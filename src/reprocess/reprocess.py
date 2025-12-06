from src.util.const import SELECT_TICKET
from loguru import logger

from src.util.requester import get_data


def reprocess_data(tickets, start, end):
    for ticket in tickets:
        data = get_data(ticket, start, end)
        data['Date'] = data['Date'].dt.tz_convert('UTC').dt.tz_localize(None)
        data.rename(columns={'Stock Splits': 'Stock_Splits'}, inplace=True)

        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            logger.error(f"Missing columns for ticket {ticket}: {missing_columns}")
            continue

        # Select required columns
        data = data[required_columns]
        data['Ticket'] = ticket

        # Write data to Athena Iceberg
        try:
            wr.athena.to_iceberg(
                df=data,
                database='corretagem',
                table='stock_data',
                temp_path='s3://finance-605771322130/temp/',
                table_location='s3://finance-605771322130/raw/stock_data/',
                keep_files=False,
            )
            logger.success(f'Finished processing {ticket}')
        except Exception as e:
            logger.error(f"Athena write error for ticket {ticket}: {e}")


if __name__ == "__main__":
    start = "2024-01-01"
    end = "2025-12-31"
    reprocess_data(SELECT_TICKET, start, end)
