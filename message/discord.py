import requests

URL = 'https://discord.com/api/webhooks/1332777736858505309/GLUQS9nKLw04eSFKVvkcLXQk2K6YozXuffCdRRTKmPEttk1HSiCLCNZq9KuIULYljK1p'

def parser_sucess_msg(tickets: list[str], start: str, end: str) -> str:
    return f"Tickets: {tickets}.\nStart Date: {start}.\nEnd Date: {end}"

def parser_fail_msg(error: str, ticket: str):
    return f"Ticket: {ticket}.\nError: {error}"

def send_discord(msg: str, url: str = URL):
    data = {
        "username": "Financa Cloud Functions",
        "avatar_url": "https://i.imgur.com/NiTuE1J.jpeg",
        "content": msg
    }
    requests.post(url, json=data)