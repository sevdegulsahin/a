# 🌿 Carbon Footprint Calculator Prediction & Suggestions With GenAI

Based on the information provided by the user, their carbon footprint is predicted, and environment-friendly suggestions are generated using GenAI according to the user's carbon footprint value. The user's information is then stored in the database

- The data on the https://greenmetric.ui.ac.id/ website was examined, and a synthetic dataset was created based on various calculations using carbon emission coefficients. This generated dataset was then merged with the carbon_emission.csv dataset.


- In the dataset section, various processes were carried out such as exploratory data analysis, data preprocessing, scaling, feature engineering, outlier detection, correlation analysis, training of various models, and prediction of results.


- As machine learning models, *XGBoost Regression* and *Random Forest Regression* were used initially. Later, a stacking method was applied using **StackingRegressor (XGBoost + RandomForest + LinearRegression)**.


- The data was stored using the **Supabase** database, and the recommendations were generated using the **Gemini API**.


- The connection between the user and Python–Supabase was established using **FastAPI**.


- Basic HTML and CSS files were created for user login.

---

## 🚀 Features

- Carbon Footprint Prediction
- Visualization of the user's carbon footprint value in comparison to the global average carbon footprint
- Storing data in the Supabase database
- Personalized recommendations with the Gemini API
- FastAPI-based fast REST API

---

## 🌍 Technologies Used

- **FastAPI**
- **XGBoost + RandomForest + LinearRegression** –> **StackingRegressor**
- **Pickle**
- **Supabase**
- **Gemini API**

---

---

## ⚙️ Installation

### Requirements

- **Python 3.8 or higher**
- **Git and Git LFS**
- **Supabase account and project** (for URL and API keys)
- **Google Gemini API key**

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sevdegulsahin/a.git
   cd a

### Install the requirements:
- **pip install  -r requirements.txt**

- *(fastapi uvicorn jinja2 python-multipart pandas numpy matplotlib seaborn joblib supabase google-generativeai python-dotenv xgboost scikit-learn)*

### Run the carbon_emission.py file:
- Run the carbon_emission.py file in the project using Python.
- Thus, the necessary files and predictions for the main.py file to run will be created.

### Run the application:
uvicorn main:app --reload --port 5056
The application will run locally at http://127.0.0.1:5056.
You can change the **--port** part if you wish.


## 📝 Usage

1. Fill out the form located on the homepage (`/`). The form contains questions related to lifestyle, such as diet, transportation, energy usage, gender, monthly expenses, etc.
2. *Click the "Calculate Carbon Footprint" button.
3. The results display your estimated carbon footprint *(kg CO2/year)*, a pie chart comparing it with the global average, and environment-friendly recommendations from the Gemini API.
4. Your data will be saved in the `carbon_footprints` table in the Supabase database.
---

## 📊 Dataset

**Source:** The `carbon_emission.csv` dataset contains various features for carbon footprint calculations.
- The features in the dataset were created using real-world data and various carbon emission coefficients.

### 📋 Features:
- **Numerical Features ->** Monthly Grocery Bill, Vehicle Monthly Distance Km, Waste Bag Weekly Count, How Long TV PC Daily Hour, How Many New Clothes Monthly, How Long Internet Daily Hour, CarbonEmission.


- **Categorical Features ->** Body Type, Sex, Diet, How Often Shower, Heating Energy Source, Transport, Vehicle Type, Social Activity, Frequency of Traveling by Air, Waste Bag Size, Energy efficiency, Recycling, Cooking_With

### 🚧 Preprocessing:
- Categorical data was transformed using **OneHotEncoder**
- Numerical data was scaled using **StandardScaler**
- `Recycling` and `Cooking_With` columns were converted from string lists to flat strings. *(eval)*
- Null values in the `Vehicle Type` column were filled with **None**

---

## 🦾 Machine Learning Models

- **Models ->** 
  - *XGBoost Regressor* and *RandomForest Regressor* were combined using **Stacking Regressor**, with XGBoost Regressor and RandomForest Regressor used as base models.
  - *Linear Regression* was used as the meta model, resulting in a model accuracy of **97.42%.**


- **Train ->** The dataset was split into 80% training and 20% testing.
  - A more general result was obtained, and to prevent the risk of overfitting and underfitting, *shuffle=True* was used.


### 🟰 Performance Metrics:
- **Mean Absolute Error (MAE)**
- **Mean Squared Error (MSE)**
- **R2 Score**


- Additionally, **log_loss** results were checked for all models..

### 📁 Saved Files:
- `stacking_model.pkl`: Trained **Stacking Regressor** model.
- `ohe.pkl`: **OneHotEncoder** object.
- `standard_scalers.pkl`: **StandardScaler** object.

---

## 🗃️ Supabase Database

- User inputs and prediction results are saved in the `carbon_footprints` table.


- It has been chosen for this project due to its cloud-based nature, fast processing capabilities, and ease of use.


## 🤖 Gemini API

- Based on the data provided by the user, the Gemini API generates personalized environment-friendly recommendations according to the calculated carbon footprint value.


- The recommendations are tailored according to low, average, or high carbon footprint levels and presented to the user.



## 🧑‍💻 Workers on the project
- Bora Eren Erdem -> https://github.com/BoraErenErdem
- Sevde Gül Şahin -> https://github.com/sevdegulsahin
- Deniz Su Şen -> https://github.com/Sen-denizsu
- Ahmet Reşat Keyan -> https://github.com/Drandalll