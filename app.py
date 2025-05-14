from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
DB_PATH = 'dtp.db'

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
        geo_url = f'https://geocode-maps.yandex.ru/1.x/?apikey=391e84dc-21f8-4978-b1ec-45fc67e8bde3&geocode={address}&format=json'
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

if __name__ == '__main__':
    app.run(debug=True)