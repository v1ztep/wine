from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

WINERY_BASE_YEAR = 1920
now_year = datetime.datetime.now().year
delta = now_year - WINERY_BASE_YEAR

parser = argparse.ArgumentParser(description='Optional argument path to excel file')
parser.add_argument(
    '--path',
    type=str,
    default=os.getenv('DEFAULT_PATH_TO_EXCEL_FILE', 'wine.xlsx'),
    help='provide an path to excel file'
)
path_to_excel = parser.parse_args()

excel_data_df = pd.read_excel(path_to_excel.path,
                              usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
                              keep_default_na=False)
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
