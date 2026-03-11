from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server, shell





def on_reload():
    template = env.get_template('template.html')
    with open('meta_data.json', 'r', encoding="utf-8") as file:
        books_data = file.read()
        books = json.loads(books_data)

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)

if __name__ == '__main__':
    env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
    )
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()