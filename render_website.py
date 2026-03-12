from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import math

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


BOOK_ON_PAGE = 10
BOOK_IN_ROW = 2


def on_reload():
    template = env.get_template('template.html')
    os.makedirs('pages', exist_ok=True)
    with open('meta_data.json', 'r', encoding="utf-8") as file:
        books_data = file.read()
    books = json.loads(books_data)
    books_by_pages = list(chunked(books, BOOK_ON_PAGE))
    pages_number = math.ceil(len(books) / BOOK_ON_PAGE)

    for page_num, books_on_page in enumerate(books_by_pages, 1):
        books_by_rows = list(chunked(books_on_page, BOOK_IN_ROW))
        rendered_page = template.render(
            book_rows=books_by_rows,
            pages_number=pages_number,
            current_page=page_num
        )

        with open(
            f'pages/index{page_num}.html',
            'w',
            encoding="utf-8"
        ) as file:
            file.write(rendered_page)

if __name__ == '__main__':
    env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
    )
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename="pages/index1.html")

# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()