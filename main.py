from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd


WINERY_BASE_YEAR = datetime.datetime(year=1920, month=1, day=1, hour=0).year
now_year = datetime.datetime.now().year
delta = now_year - WINERY_BASE_YEAR

excel_data_df = pd.read_excel('wine.xlsx', usecols=['Название','Сорт','Цена','Картинка'])
wines_dict = excel_data_df.to_dict(orient='record')

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    winery_age=f"Уже {delta} лет с вами",
    wines=wines_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()