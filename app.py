from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import urllib.parse

# Создаем экземпляр Flask приложения
app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов
DB_PATH = 'dtp.db'
API_KEY = "7ebca4eb-7e57-4d26-8957-ea7a04fbdead"

# Пример данных: координаты опасных зон в Краснодаре
danger_zones = [
    {"lat": 45.0448, "lon": 38.9760, "count": 20},  # Центр города
    {"lat": 45.0600, "lon": 38.9800, "count": 30},  # Северная часть
    {"lat": 45.0350, "lon": 38.9650, "count": 25},  # Южная часть
    {"lat": 45.0480, "lon": 38.9850, "count": 15},  # Восточная часть
    {"lat": 45.0400, "lon": 38.9700, "count": 10},  # Западная часть
]

def get_coordinates(address):
    # URL кодируем адрес
    encoded_address = urllib.parse.quote(address)
    # Используем JSON формат с API ключом
    geo_url = f'https://geocode-maps.yandex.ru/1.x/?format=json&apikey={API_KEY}&geocode={encoded_address}'
    print(f"Geocoding URL: {geo_url}")
    try:
        geo_resp = requests.get(geo_url)
        if geo_resp.status_code != 200:
            print(f"Error response from geocoder: {geo_resp.text}")
            return None
        geo_data = geo_resp.json()
        feature_members = geo_data['response']['GeoObjectCollection']['featureMember']
        if not feature_members:
            print(f"No features found for address: {address}")
            return None
        pos = feature_members[0]['GeoObject']['Point']['pos']
        coords = pos.split()
        return [float(coords[1]), float(coords[0])]
    except Exception as e:
        print(f"Geocoding error for address {address}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')  # Рендерим HTML из папки templates

@app.route('/data')
def get_data():
    return jsonify(danger_zones)

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

@app.route('/api/route', methods=['POST'])
def get_route():
    try:
        data = request.json
        if not data:
            print("Error: No JSON data received")
            return jsonify({'error': 'Не получены данные запроса'}), 400

        start_address = data.get('start')
        end_address = data.get('end')
        
        if not start_address or not end_address:
            print("Error: Missing start or end address")
            return jsonify({'error': 'Не указан начальный или конечный адрес'}), 400
        
        print(f"Processing request - Start: {start_address}, End: {end_address}")
        
        # Добавляем "Краснодар" к адресам, если не указан город
        if 'краснодар' not in start_address.lower():
            start_address = f"Краснодар, {start_address}"
        if 'краснодар' not in end_address.lower():
            end_address = f"Краснодар, {end_address}"
            
        print(f"Modified addresses - Start: {start_address}, End: {end_address}")
        
        start_coords = get_coordinates(start_address)
        if not start_coords:
            print(f"Error: Could not geocode start address: {start_address}")
            return jsonify({'error': f'Не удалось определить координаты начального адреса: {start_address}'}), 400
            
        end_coords = get_coordinates(end_address)
        if not end_coords:
            print(f"Error: Could not geocode end address: {end_address}")
            return jsonify({'error': f'Не удалось определить координаты конечного адреса: {end_address}'}), 400
        
        print(f"Successfully geocoded - Start: {start_coords}, End: {end_coords}")

        # Получаем все точки ДТП
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT address FROM dtp')
            dtp_addresses = c.fetchall()
            conn.close()
        except Exception as e:
            print(f"Database error: {str(e)}")
            return jsonify({'error': 'Ошибка при получении данных о ДТП'}), 500

        # Получаем координаты всех точек ДТП
        dtp_points = []
        for address in dtp_addresses:
            coords = get_coordinates(address[0])
            if coords:
                dtp_points.append(coords)
                
        print(f"Found {len(dtp_points)} DTP points")

        # Формируем ответ с координатами
        response = {
            'start': start_coords,
            'end': end_coords,
            'dtp_points': [{'lat': point[0], 'lon': point[1]} for point in dtp_points]
        }
        
        print(f"Sending response: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Произошла ошибка при обработке запроса: {str(e)}'}), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)