import yfinance as yf

from message.discord import send_discord
from message.render_jinja import daily_earning
from util.transformation import get_daily_return, transform_data

ticket = 'B5P211.SA'
start = '2025-01-01'
end = '2025-01-04'

data = yf.Ticker(ticket).history(start=start, end=end).reset_index()
data_trans = transform_data(data, ticket)
d = get_daily_return(data_trans)
msg = daily_earning(d)
send_discord(msg)