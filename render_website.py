import json
import os
import math
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


BOOK_IN_ROW = 2


def get_cmd_args():
    parser = argparse.ArgumentParser(
        description='Запускает локальный сервер и отслеживает изменения.',
    )
    parser.add_argument(
        '-t',
        '--template',
        type=str,
        default='template.html',
        help='Путь к шаблону для отрисовки и отслеживания с расширением.'
    )
    parser.add_argument(
        '-bf',
        '--books_file',
        type=str,
        default='meta_data.json',
        help='Имя и путь до файла с данными о книгах.',
    )
    parser.add_argument(
        '-bop',
        '--book_on_page',
        type=int,
        default=10,
        help='Количество книг отображаемых на одной странице.',
    )
    args = parser.parse_args()
    return args


def on_reload(book_on_page, template, books_file):
    template = env.get_template(template)
    os.makedirs('pages', exist_ok=True)
    with open(books_file, 'r', encoding="utf-8") as file:
        books = json.load(file)
    books_by_pages = list(chunked(books, book_on_page))
    pages_number = math.ceil(len(books) / book_on_page)

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

    args = get_cmd_args()

    on_reload(
        book_on_page=args.book_on_page,
        template=args.template,
        books_file=args.books_file,
    )

    server = Server()
    server.watch(args.template, on_reload)
    server.serve(root='.', default_filename="pages/index1.html")
