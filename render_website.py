from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

with open('meta_data.json', 'r', encoding="utf8") as file:
    books_data = file.read()
books = json.loads(books_data)

rendered_page = template.render(books=books)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()