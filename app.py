from flask import Flask, request, jsonify, render_template
from config import Config
import google.generativeai as genai
from datetime import datetime
import bcrypt


app = Flask(__name__)

# Bellekte veri saklama
users = []  # Kullanıcılar: [{'id': 1, 'username': '...', 'email': '...', 'password_hash': '...'}]
records = []  # Kayıtlar: [{'id': 1, 'user_id': 1, 'date': '...', 'energy_kwh': ..., 'transport_km': ..., 'food_type': '...', 'co2e_kg': ..., 'recommendation': '...'}]
user_id_counter = 1
record_id_counter = 1

# Gemini API yapılandırması
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    global user_id_counter
    data = request.json
    try:
        # Kullanıcı adı veya e-posta zaten var mı?
        if any(user['username'] == data['username'] or user['email'] == data['email'] for user in users):
            return jsonify({'error': 'Kullanıcı adı veya e-posta zaten kayıtlı'}), 400

        # Parolayı hash'le
        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = {
            'id': user_id_counter,
            'username': data['username'],
            'email': data['email'],
            'password_hash': hashed.decode('utf-8')
        }
        users.append(user)
        user_id_counter += 1
        return jsonify({'message': 'Kullanıcı başarıyla kaydedildi', 'user_id': user['id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate', methods=['POST'])
def calculate_footprint():
    global record_id_counter
    data = request.json
    try:
        energy_kwh = float(data['energy_kwh'])
        transport_km = float(data['transport_km'])
        food_type = data['food_type']
        user_id = int(data['user_id'])

        # Kullanıcı var mı?
        if not any(user['id'] == user_id for user in users):
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 400

        # Basit emisyon faktörleri
        energy_factor = 0.5  # kg CO2e/kWh
        transport_factor = 0.2  # kg CO2e/km
        food_factors = {'vegetarian': 2.0, 'meat': 15.0}  # kg CO2e/kg
        co2e = (energy_kwh * energy_factor) + (transport_km * transport_factor) + food_factors.get(food_type, 2.0)

        # Gemini API ile öneri al
        prompt = f"Kullanıcının karbon ayak izi {co2e:.2f} kg CO2e. Çevresel etkisini azaltmak için 3 kısa, pratik öneri sunn."
        response = model.generate_content(prompt)
        recommendation = response.text

        # Bellekte sakla
        record = {
            'id': record_id_counter,
            'user_id': user_id,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'energy_kwh': energy_kwh,
            'transport_km': transport_km,
            'food_type': food_type,
            'co2e_kg': co2e,
            'recommendation': recommendation
        }
        records.append(record)
        record_id_counter += 1

        return jsonify({'co2e': co2e, 'recommendation': recommendation})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)