

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import joblib
from typing import List
import matplotlib.pyplot as plt
import base64
import io
import seaborn as sns
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import google.generativeai as genai


# .env dosyasını yükle
load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def get_gemini_recommendation(prediction):
    prompt = f"""
    Kullanıcının yıllık karbon ayak izi {prediction:.2f} kg CO2. 
    Bu değeri değerlendir ve kullanıcıya yaşam tarzını nasıl iyileştirebileceği konusunda öneriler ver. 
    Sayısal analiz ve çevre dostu davranışlar üzerine mantıklı, motive edici bir açıklama yaz.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# Jinja2 şablonları
templates = Jinja2Templates(directory="templates")

# Supabase bağlantısını yapalım
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Model, OHE ve Scaler yükleme
BASE_DIR = os.path.dirname(__file__)
model = joblib.load(os.path.join(BASE_DIR, "stacking_model.pkl"))
ohe = joblib.load("ohe.pkl")
scalers = joblib.load("standard_scalers.pkl")

# numerical ve categorical sütunlar
num_cols = [
    'Monthly Grocery Bill', 'Vehicle Monthly Distance Km', 'Waste Bag Weekly Count',
    'How Long TV PC Daily Hour', 'How Many New Clothes Monthly', 'How Long Internet Daily Hour'
]
cat_cols = [
    'Body Type', 'Sex', 'Diet', 'How Often Shower', 'Heating Energy Source', 'Transport', 
    'Vehicle Type', 'Social Activity', 'Frequency of Traveling by Air', 'Waste Bag Size', 
    'Energy efficiency', 'Recycling', 'Cooking_With'
]

def preprocess_user_input(user_input):
    # Categoric verileri işleme
    categorical_data = pd.DataFrame({col: [user_input.get(col, 'None')] for col in cat_cols})
    for col in ['Recycling', 'Cooking_With']:
        if isinstance(categorical_data[col][0], list):
            categorical_data[col] = ','.join(categorical_data[col][0]) if categorical_data[col][0] else 'None'
    categorical_encoded = ohe.transform(categorical_data[cat_cols])
    categorical_encoded_df = pd.DataFrame(categorical_encoded, columns=ohe.get_feature_names_out(cat_cols))

    # Numerik verileri işleme
    numerical_data = pd.DataFrame({col: [float(user_input.get(col, 0))] for col in num_cols})
    for col in num_cols:
        if col in scalers:
            numerical_data[col] = scalers[col].transform(numerical_data[[col]])

    # Veriyi birleştirme
    processed_data = pd.concat([numerical_data, categorical_encoded_df], axis=1)
    for col in model.feature_names_in_:
        if col not in processed_data.columns:
            processed_data[col] = 0
    processed_data = processed_data[model.feature_names_in_]

    return processed_data

def carbon_footprint_graph(prediction):
    plt.figure(figsize=(7, 7))
    values = [prediction, 4800]
    plt.pie(values, labels=['Your Carbon Footprint', 'Global Average'], colors=sns.color_palette('Set2'), autopct='%1.2f%%', startangle=90, shadow=True, explode=[0.05, 0.05], textprops={'fontsize': 12})
    plt.ylabel('Carbon Footprint (kg CO2/year)', )
    plt.title('Your Carbon Footprint Comparison')
    plt.axis('equal')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    
    return graphic

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index_bora.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    
    request: Request,
    Body_Type: str = Form(...),
    Sex: str = Form(...),
    Diet: str = Form(...),
    How_Often_Shower: str = Form(...),
    Heating_Energy_Source: str = Form(...),
    Transport: str = Form(...),
    Vehicle_Type: str = Form(default="None"),
    Social_Activity: str = Form(...),
    Monthly_Grocery_Bill: float = Form(default=0),
    Frequency_of_Traveling_by_Air: str = Form(...),
    Vehicle_Monthly_Distance_Km: float = Form(default=0),
    Waste_Bag_Size: str = Form(...),
    Waste_Bag_Weekly_Count: float = Form(default=0),
    How_Long_TV_PC_Daily_Hour: float = Form(default=0),
    How_Many_New_Clothes_Monthly: float = Form(default=0),
    How_Long_Internet_Daily_Hour: float = Form(default=0),
    Energy_efficiency: str = Form(...),
    Recycling: List[str] = Form(default=[]),
    Cooking_With: List[str] = Form(default=[])
    
):

    try:
        # Kullanıcıdan gelen inputları alalım
        user_input = {
            'Body Type': Body_Type,
            'Sex': Sex,
            'Diet': Diet,
            'How Often Shower': How_Often_Shower,
            'Heating Energy Source': Heating_Energy_Source,
            'Transport': Transport,
            'Vehicle Type': Vehicle_Type,
            'Social Activity': Social_Activity,
            'Monthly Grocery Bill': Monthly_Grocery_Bill,
            'Frequency of Traveling by Air': Frequency_of_Traveling_by_Air,
            'Vehicle Monthly Distance Km': Vehicle_Monthly_Distance_Km,
            'Waste Bag Size': Waste_Bag_Size,
            'Waste Bag Weekly Count': Waste_Bag_Weekly_Count,
            'How Long TV PC Daily Hour': How_Long_TV_PC_Daily_Hour,
            'How Many New Clothes Monthly': How_Many_New_Clothes_Monthly,
            'How Long Internet Daily Hour': How_Long_Internet_Daily_Hour,
            'Energy efficiency': Energy_efficiency,
            'Recycling': Recycling,
            'Cooking_With': Cooking_With
        }

        # Inputları işleyelim
        processed_data = preprocess_user_input(user_input)

        # XGBoost Regression modelini kullanarak tahmin yapalım
        prediction = model.predict(processed_data)[0]

        # Grafik oluşturma
        plot_data = carbon_footprint_graph(prediction)

        # Sonuçları Supabase veritabanına kaydetme
        supabase.table('carbon_footprints').insert({
            "body_type": Body_Type,
            "sex": Sex,
            "diet": Diet,
            "carbon_footprint": prediction
        }).execute()
        recommendation = get_gemini_recommendation(prediction)
        return templates.TemplateResponse(
    "index_bora.html",
    {
        "request": request,
        "prediction": f"Estimated Carbon Emission: {prediction:.2f} kg CO2/year",
        "plot_data": plot_data,
        "recommendation": recommendation
    }
)

    except Exception as e:
        return templates.TemplateResponse(
            "index_bora.html",
            {"request": request, "prediction": f"Error: {str(e)}", "plot_data": None}
        )
