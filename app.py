from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3
import random
from datetime import datetime, timedelta
import urllib.parse

app = Flask(__name__)
CORS(app)
DB_PATH = 'dtp.db'
API_KEY = "7ebca4eb-7e57-4d26-8957-ea7a04fbdead"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dtp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        address TEXT,
        injured INTEGER
    )''')
    c.execute('DELETE FROM dtp')
    conn.commit()
    conn.close()

def fill_random_dtps():
    streets = [
        'Красная', 'Северная', 'Ставропольская', 'Калинина', 'Тургенева',
        'Гагарина', 'Зиповская', '40 лет Победы', 'Мачуги', 'Дзержинского',
        'Будённого', 'Коммунаров', 'Ленина', 'Мира', 'Головатого',
        'Седина', 'Пушкина', 'Чапаева', 'Яна Полуяна', 'Московская'
    ]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for _ in range(50):
        date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        time_ = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
        street = random.choice(streets)
        house = str(random.randint(10, 50))
        address = f"{street}, {house}"
        injured = random.randint(0, 1)
        c.execute('INSERT INTO dtp (date, time, address, injured) VALUES (?, ?, ?, ?)',
                  (date, time_, address, injured))
    conn.commit()
    conn.close()

def get_coordinates(address):
    encoded_address = urllib.parse.quote(address)
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

init_db()
fill_random_dtps()

@app.route('/api/dtp', methods=['GET'])
def get_dtp_points():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT date, time, address, injured FROM dtp')
    rows = c.fetchall()
    conn.close()
    points = []
    for row in rows:
        date, time_, address, injured = row
        geo_url = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'
        try:
            geo_resp = requests.get(geo_url)
            geo_data = geo_resp.json()
            feature_members = geo_data['response']['GeoObjectCollection']['featureMember']
            if not feature_members:
                continue
            pos = feature_members[0]['GeoObject']['Point']['pos']
            lon, lat = map(float, pos.split())
            points.append({
                'lat': lat,
                'lon': lon,
                'desc': f'{date} {time_}, {address}, Пострадавшие: {"Да" if injured else "Нет"}'
            })
        except Exception:
            continue
    return jsonify(points)

@app.route('/api/dtp', methods=['POST'])
def add_dtp():
    data = request.json
    date = data.get('date')
    time_ = data.get('time')
    address = data.get('address')
    injured = 1 if data.get('injured') else 0
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO dtp (date, time, address, injured) VALUES (?, ?, ?, ?)',
              (date, time_, address, injured))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/dtp/list', methods=['GET'])
def get_dtp_list():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT date, time, address, injured FROM dtp ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        date, time_, address, injured = row
        result.append({
            'date': date,
            'time': time_,
            'address': address,
            'injured': bool(injured)
        })
    return jsonify(result)

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
        
        # Используем глобальную функцию get_coordinates с apikey
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

if __name__ == '__main__':
    app.run(debug=True)