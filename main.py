from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd


WINERY_BASE_YEAR = 1920
now_year = datetime.datetime.now().year
delta = now_year - WINERY_BASE_YEAR

excel_data_df = pd.read_excel('wine.xlsx', usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'], keep_default_na=False)
unique_wine_categories = excel_data_df.Категория.unique()
wines_info = excel_data_df.to_dict(orient='record')


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    winery_age=f"Уже {delta} лет с вами",
    unique_wine_categories=unique_wine_categories,
    wines_info=wines_info
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()