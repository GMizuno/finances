import requests


def parser_sucess_msg(tickets: list[str], start: str, end: str) -> str:
    return f"Tickets: {tickets}.\nStart Date: {start}.\nEnd Date: {end}\nOrigin: AWS Lambda"


def parser_fail_msg(error: str, ticket: str):
    return f"Ticket: {ticket}.\nError: {error}"


def send_discord(msg: str, url: str):
    data = {
        "username": "Financa Cloud Functions",
        "avatar_url": "https://i.imgur.com/NiTuE1J.jpeg",
        "content": msg,
    }
    if url != "":
        requests.post(url, json=data)
