from crypt import methods

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
from supabase import create_client, Client

supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        # Eşsiz kullanıcı kontrolü
        existing = supabase.table("users").select("*").eq("email", data["email"]).execute()
        if existing.data:
            return jsonify({'error': 'Bu e-posta zaten kayıtlı'}), 400

        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        response = supabase.table("users").insert({
            'username': data['username'],
            'email': data['email'],
            'password_hash': hashed
        }).execute()
        user_id = response.data[0]['id']
        return jsonify({'message': 'Kayıt başarılı', 'user_id': user_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate', methods=['POST'])
def calculate_footprint():
    data = request.json
    try:
        user_id = int(data['user_id'])

        # Kullanıcı kontrolü
        user_check = supabase.table("users").select("*").eq("id", user_id).execute()
        if not user_check.data:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 400

        energy_kwh = float(data['energy_kwh'])
        transport_km = float(data['transport_km'])
        food_type = data['food_type']
        food_factors = {'vegetarian': 2.0, 'meat': 15.0}
        co2e = (energy_kwh * 0.5) + (transport_km * 0.2) + food_factors.get(food_type, 2.0)

        # Gemini API ile öneri
        prompt = f"Kullanıcının karbon ayak izi {co2e:.2f} kg CO2e. Çevresel etkisini azaltmak için 3 kısa, pratik öneri sun."
        recommendation = model.generate_content(prompt).text

        # Supabase'e kayıt ekle
        supabase.table("records").insert({
            'user_id': user_id,
            'date': datetime.now().isoformat(),
            'energy_kwh': energy_kwh,
            'transport_km': transport_km,
            'food_type': food_type,
            'co2e_kg': co2e,
            'recommendation': recommendation
        }).execute()

        return jsonify({'co2e': co2e, 'recommendation': recommendation})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)