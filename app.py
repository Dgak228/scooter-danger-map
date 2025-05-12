from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3

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
        street TEXT,
        house TEXT,
        injured INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/dtp', methods=['GET'])
def get_dtp_points():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT date, time, street, house, injured FROM dtp')
    rows = c.fetchall()
    conn.close()
    points = []
    for row in rows:
        date, time_, street, house, injured = row
        address = f'Краснодар, {street} {house}'
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
                'desc': f'{date} {time_}, {street} {house}, Пострадавшие: {"Да" if injured else "Нет"}'
            })
        except Exception:
            continue
    return jsonify(points)

@app.route('/api/dtp', methods=['POST'])
def add_dtp():
    data = request.json
    date = data.get('date')
    time_ = data.get('time')
    street = data.get('street')
    house = data.get('house')
    injured = 1 if data.get('injured') else 0
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO dtp (date, time, street, house, injured) VALUES (?, ?, ?, ?, ?)',
              (date, time_, street, house, injured))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/dtp/list', methods=['GET'])
def get_dtp_list():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT date, time, street, house, injured FROM dtp ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        date, time_, street, house, injured = row
        result.append({
            'date': date,
            'time': time_,
            'street': street,
            'house': house,
            'injured': bool(injured)
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)