from pandas_gbq import read_gbq



def delete_row_based_date_and_ticket(table: str, start_date: str, end_date: str, ticket:str, project: str):
    query = f"""
    DELETE
    FROM `{table}`
    WHERE `Date` BETWEEN "{start_date}" AND "{end_date}" AND Ticket = "{ticket}"
    """
    print(f'Running query {query}')
    read_gbq(query, project_id=project)
