import pendulum
import awswrangler as wr
import os
from dotenv import load_dotenv

load_dotenv()

from src.util.requester import get_data
from src.util.log import logger


def main() -> str:
    logger.info('Starting the process')
    tickets = os.getenv('TICKETS').split(',')

    logger.info(f'Extracting these {tickets}')
    for ticket in tickets:
        logger.info(f'Processing {ticket}')
        start = '2024-01-01'# pendulum.today().subtract(days=2).to_date_string()
        end =  '2025-12-05'# pendulum.today().subtract(days=1).to_date_string()

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

    return ""

if __name__ == '__main__':
    main()
