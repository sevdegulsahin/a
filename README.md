# 🌿 Carbon Footprint Predictor API

Bu proje, kullanıcı girdilerine göre karbon ayak izini tahmin eden ve çevre dostu öneriler sunan bir RESTful API'dir.  
Makine öğrenimi modeli olarak **StackingRegressor (XGBoost + RandomForest + LinearRegression)** kullanılmıştır.  
Veriler **Supabase** ile saklanır, öneriler **Gemini API** ile oluşturulur.

---

## 🚀 Özellikler

- Karbon ayak izi tahmini
- Supabase veritabanına kayıt
- Gemini API ile kişiselleştirilmiş öneriler
- FastAPI tabanlı hızlı REST API

---

## 🧠 Kullanılan Teknolojiler

- **FastAPI** – Modern ve yüksek performanslı web framework
- **XGBoost, RandomForest, LinearRegression** – StackingRegressor yapısı
- **Pickle** – Model serileştirme
- **Supabase** – Bulut veritabanı
- **Gemini API** – Öneri üretimi için yapay zeka servisi

---

## 📁 Proje Yapısı

carbon-footprint-api/
├── main.py
├── model_training.py
├── stacking_model.pkl
├── ohe.pkl
├── standard_scalers.pkl
├── .env
├── requirements.txt
└── README.md

---

## ⚙️ Kurulum

### Gereksinimler

- **Python 3.8 veya üzeri**
- **Git**
- **Supabase hesabı ve proje** (URL ve API anahtarı için)
- **Google Gemini API anahtarı**

### Adımlar

1. **Depoyu Klonlayın:**

   ```bash
   git clone https://github.com/sevdegulsahin/a.git
   cd a
   
### Sanal Ortam Oluşturun ve Etkinleştirin:
python -m venv .venv
source .venv/bin/activate  # Windows için: .venv\Scripts\activate

### Bağımlılıkları Yükleyin:
pip install  -r requirements.txt 
(fastapi uvicorn jinja2 python-multipart pandas numpy matplotlib seaborn joblib supabase google-generativeai python-dotenv xgboost scikit-learn)

### Uygulamayı Çalıştırın:
uvicorn main:app --reload --port 5056
Uygulama http://127.0.0.1:5056 adresinde çalışacaktır.
--reload bayrağı, geliştirme sırasında dosya değişikliklerini otomatik olarak algılar.

**📝 Kullanım**
Ana sayfada (/) bulunan formu doldurun. Form, yaşam tarzınıza ilişkin soruları içerir (örneğin, diyet, ulaşım, enerji kullanımı).
"Calculate Carbon Footprint" butonuna tıklayın.
Sonuçlar, tahmini karbon ayak izinizi (kg CO2/yıl), küresel ortalamayla karşılaştırmalı bir grafik ve Gemini API'den gelen çevre dostu önerileri gösterecektir.
Verileriniz Supabase veritabanındaki carbon_footprints tablosuna kaydedilir.

**📊 Veri Seti**
Kaynak: carbon_emission.csv veri seti, karbon ayak izi hesaplamaları için çeşitli özellikler içerir.

**Özellikler:**
Sayısal: Aylık market harcaması, araçla katedilen mesafe, çöp torbası sayısı, TV/PC kullanım süresi, vb.
Kategorik: Vücut tipi, cinsiyet, diyet, duş sıklığı, ulaşım türü, vb.
Ön İşleme:
Kategorik veriler OneHotEncoder ile kodlandı.
Sayısal veriler StandardScaler ile ölçeklendirildi.
Recycling ve Cooking_With sütunları string listelerden düz stringlere dönüştürüldü.
Vehicle Type sütunundaki null değerler None ile dolduruldu.

**🧪 Makine Öğrenimi Modeli**

Modeller: XGBoost Regressor ve RandomForest Regressor, Stacking Regressor ile birleştirilmiştir.
Eğitim: Veri seti %80 eğitim, %20 test olarak bölündü.
Performans Metrikleri:
Ortalama Mutlak Hata (MAE)
Ortalama Kare Hata (MSE)
R² Skoru
Kaydedilen Dosyalar:
stacking_model.pkl: Eğitilmiş Stacking Regressor modeli.
ohe.pkl: OneHotEncoder nesnesi.
standard_scalers.pkl: StandardScaler nesneleri.

**🗃️ Supabase Veritabanı**

Kullanıcı girdileri ve tahmin sonuçları carbon_footprints tablosuna kaydedilir.


**🤖 Gemini API**

Gemini API, kullanıcının karbon ayak izine göre özelleştirilmiş çevre dostu öneriler üretir.
Öneriler, düşük, ortalama veya yüksek karbon ayak izine göre uyarlanır ve Türkçe olarak sunulur.

