"""
ljhmjj event tracker - Flask + SQLite backend
Deploy: python server.py (runs on port 5000)
"""
import sqlite3, json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database setup
def get_db():
    db = sqlite3.connect('events.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        time TEXT NOT NULL,
        scene TEXT NOT NULL,
        type TEXT NOT NULL,
        event TEXT NOT NULL
    )''')
    db.commit()
    db.close()

init_db()

@app.route('/api/events', methods=['GET'])
def list_events():
    db = get_db()
    events = db.execute('SELECT * FROM events ORDER BY id DESC').fetchall()
    db.close()
    return jsonify([dict(e) for e in events])

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO events (id, time, scene, type, event) VALUES (?, ?, ?, ?, ?)',
        [data['id'], data['time'], data['scene'], data['type'], data['event']])
    db.commit()
    db.close()
    return jsonify({'status': 'ok'})

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    db = get_db()
    db.execute('DELETE FROM events WHERE id = ?', [event_id])
    db.commit()
    db.close()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
