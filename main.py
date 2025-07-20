from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Розбираємо URL на компоненти
        pr_url = urllib.parse.urlparse(self.path)

        # Якщо шлях відповідає головній сторінці, відправляємо файл index.html
        if pr_url.path == '/':
            self.send_html_file('index.html')

        # Якщо шлях відповідає сторінці пошуку, відправляємо файл search.html
        elif pr_url.path == '/search':
            self.send_html_file('search.html')

        # Перевіряємо, чи існує файл за вказаним шляхом, і якщо так, відправляємо його як статичний ресурс
        elif pathlib.Path().joinpath(pr_url.path[1:]).exists():
            self.send_static()

        # Якщо жодна з умов не виконується, відправляємо сторінку помилки з кодом 404
        else:
            self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        """Відправка HTML-файлу."""
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            with open(filename, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_html_file('error.html', 404)

    def send_static(self):
        """Відправка статичних файлів (CSS, зображення тощо)."""
        # Відправляємо код відповіді 200, що означає успішну обробку запиту
        self.send_response(200)

        # Визначаємо тип файлу за допомогою модуля mimetypes
        mt = mimetypes.guess_type(self.path)

        # Якщо тип файлу визначено, встановлюємо відповідний заголовок Content-type
        if mt[0]:
            self.send_header("Content-type", mt[0])
        else:
            # Якщо тип файлу не визначено, використовуємо загальний тип для бінарних даних
            self.send_header("Content-type", 'application/octet-stream')

        # Завершуємо заголовки
        self.end_headers()

        try:
            # Відкриваємо файл у бінарному режимі та відправляємо його вміст клієнту
            with open(f'.{self.path}', 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            # Якщо файл не знайдено, відправляємо сторінку помилки з кодом 404
            self.send_html_file('error.html', 404)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    """Запуск локального сервера."""
    server_address = ('', 8080)  # Сервер працює на порту 8080
    http = server_class(server_address, handler_class)
    try:
        print("Server is running on <http://localhost:8080>")
        http.serve_forever()
    except KeyboardInterrupt:
        print("\nThe server has been stopped")
        http.server_close()


if __name__ == '__main__':
    run()