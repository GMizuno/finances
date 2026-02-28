import json

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

from src.util.secret import get_secret


def get_bigquery_client(secret_name: str = "glue/bigquery") -> bigquery.Client:
    """
    Creates and returns a BigQuery client using credentials from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager containing BigQuery credentials JSON

    Returns:
        bigquery.Client: Authenticated BigQuery client instance
    """
    credentials_json = get_secret(secret_name)
    credentials_dict = json.loads(credentials_json)

    print(f"Using {credentials_dict['client_email']}")
    print(f"Project ID: {credentials_dict.get('project_id')}")

    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    client = bigquery.Client(credentials=credentials, project=credentials_dict.get("project_id"))

    return client


def truncate_and_insert(client: bigquery.Client, ticket: str, df: pd.DataFrame, dataset_id: str, table_id: str) -> None:
    """
    Truncates a BigQuery table and inserts data from a pandas DataFrame.

    Args:
        client: BigQuery client instance
        df: Pandas DataFrame containing the data to insert
        dataset_id: BigQuery dataset ID
        table_id: BigQuery table ID
    """
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    truncate_query = f"DELETE FROM`{table_ref}` WHERE Ticket = '{ticket}'"
    client.query(truncate_query).result()

    # Insert data from DataFrame
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
