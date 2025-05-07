from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Пример данных: координаты опасных зон в Краснодаре
danger_zones = [
    {"lat": 45.0448, "lon": 38.9760, "count": 20},  # Центр города
    {"lat": 45.0600, "lon": 38.9800, "count": 30},  # Северная часть
    {"lat": 45.0350, "lon": 38.9650, "count": 25},  # Южная часть
    {"lat": 45.0480, "lon": 38.9850, "count": 15},  # Восточная часть
    {"lat": 45.0400, "lon": 38.9700, "count": 10},  # Западная часть
]

# Главная страница — отображает карту
@app.route('/')
def index():
    return render_template('index.html')  # Рендерим HTML из папки templates

# API для получения данных о опасных зонах
@app.route('/data')
def get_data():
    return jsonify(danger_zones)

# Маршрут для новостей
@app.route('/news')
def news():
    # URL RSS-ленты (замените на нужный источник)
    rss_url = "https://lenta.ru/rss"

    try:
        # Запрос к RSS-ленте
        response = requests.get(rss_url)
        response.raise_for_status()  # Проверка на ошибки HTTP

        # Парсинг RSS с помощью BeautifulSoup и lxml
        soup = BeautifulSoup(response.content, 'xml')

        # Извлечение новостей
        news_items = []
        for item in soup.find_all('item'):
            title = item.title.text if item.title else "Без заголовка"
            link = item.link.text if item.link else "#"
            pub_date = item.pubDate.text if item.pubDate else "Дата не указана"
            news_items.append({"title": title, "link": link, "pub_date": pub_date})

        return jsonify(news_items)

    except requests.exceptions.RequestException as e:
        # В случае ошибки возвращаем сообщение
        return jsonify([{"error": f"Ошибка при получении новостей: {str(e)}"}])

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)