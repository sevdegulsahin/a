

import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression



df = pd.read_csv('carbon_emission.csv')
df.head()
df.columns
df.shape
df.dtypes
df.dtypes.value_counts()


# Vehicle Type sütununda null değerler olduğu için bu değerleri varsayılan olarak None ile doldurdum. (buradaki sütunu categorical olarak alıp işleyeceğim için sorun teşkil etmedi)
df.isna().sum()
df['Vehicle Type'].isnull().sum()
df.replace(np.nan, 'None', inplace=True)
df['Vehicle Type'].isnull().sum()

# Recycling ve Cooking_With sütunları string liste şeklinde olduğunu bunları sonradan işleyebilmek için düz string tipine dönüştürdüm. (burada önce ast.literal_eval kullandım ancak veriyi sonradan Multi Label Binarizer ile işlemede hata veriyordu. Bu yüzden eval() ile string formatına dönüştürüp sonrasında one hot encoding uygulayarak verileri işleyebildim..!)
df['Recycling'].value_counts()
df['Cooking_With'].value_counts()

df['Recycling'] = df['Recycling'].apply(lambda x: ','.join(eval(x)) if x != 'None' else 'None')
df['Cooking_With'] = df['Cooking_With'].apply(lambda x: ','.join(eval(x)) if x != 'None' else 'None')

# categorical ve numerical sütunları belirleme
categorical_columns = df.select_dtypes(include='object').columns
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.drop('CarbonEmission')

# One Hot Encoding() ile categorical sütunları işleme
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
categorical_encoded = ohe.fit_transform(df[categorical_columns])
categorical_encoded_df = pd.DataFrame(categorical_encoded, columns=ohe.get_feature_names_out(categorical_columns), index=df.index)

# categorical sütunları kaldırıp yerine one hot encoding yapılan sütunları ekleme
df = pd.concat([df.drop(columns=categorical_columns), categorical_encoded_df], axis=1)

# numerical sütunları standardscaler() ile scale (ölçekleme) etme
ss_dict = {}
for col in numerical_columns:
    ss = StandardScaler()
    df[col] = ss.fit_transform(df[[col]])
    ss_dict[col] = ss

# Korelasyonda yanıltıcı olmaması için diagonal köşelerin korelasyonunu sıfırladım
df_corr = df.corr()
for col in range(len(df_corr)):
    df_corr.iloc[col, col] = 0.0

df_corr.head()
sns.barplot(df_corr)
sns.heatmap(df_corr, cmap='viridis')


# Özellikler (features) ve hedef değişkeni (target) belirleme
X = df.drop(columns=['CarbonEmission'])
y = df['CarbonEmission']

# train test olarak veriyi ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)

# XGBoost Regression ile model oluşturma
xgboost_reg = XGBRegressor(n_jobs=-1, random_state=42)
xgboost_reg.fit(X_train, y_train)

# oluşturulan XGBoost Regression modeline predict yaptırıp ölçüm metrikleri hesaplama
xgboost_reg_predict = xgboost_reg.predict(X_test)
print(f'XGBoost Regression Mean Absolute Error -> {mean_absolute_error(y_test, xgboost_reg_predict)}')
print(f'XGBoost Regression Mean Square Error -> {mean_squared_error(y_test, xgboost_reg_predict)}')
print(f'XGBoost Regression R2 Score -> {r2_score(y_test, xgboost_reg_predict)}')

# XGBoost Regression modelinin beklediği özellikler -> (kontrol amaçlı)
print("Modelin beklediği özellikler:", xgboost_reg.feature_names_in_.tolist())


# RandomForest Regressor modeli oluşturma
rf_reg = RandomForestRegressor(n_jobs=-1, random_state=42)
rf_reg.fit(X_train, y_train)

# oluşturulan RandomForest Regressor modeline predict yaptırıp ölçüm metrikleri hesaplama
rf_reg_predict = rf_reg.predict(X_test)
print(f'Random Forest Regression Mean Absolute Error -> {mean_absolute_error(y_test, rf_reg_predict)}')
print(f'Random Forest Regression Mean Square Error -> {mean_squared_error(y_test, rf_reg_predict)}')
print(f'Random Forest Regression R2 Score -> {r2_score(y_test, rf_reg_predict)}')


# Birden fazla model denendi ve en iyi 2 modeli (XGBoost Regression ve Random Forest Regression) Stacking yöntemi ile kullanıp üst model oluşturuldu..!
stacking_model = StackingRegressor(estimators=[('xgboost_regression', xgboost_reg), ('random_forest_regression', rf_reg)], final_estimator=LinearRegression(), cv=5, n_jobs=-1, verbose=1)
stacking_model.fit(X_train, y_train)

# oluşturulan stacking_model modelini predict yaptırıp ölçüm metrikleri hesaplama
stacking_model_predict = stacking_model.predict(X_test)
print(f'Random Forest Regression Mean Absolute Error -> {mean_absolute_error(y_test, stacking_model_predict)}')
print(f'Random Forest Regression Mean Square Error -> {mean_squared_error(y_test, stacking_model_predict)}')
print(f'Random Forest Regression R2 Score -> {r2_score(y_test, stacking_model_predict)}')


# stacking_model regression modelinin beklediği özellikler -> (kontrol amaçlı)
print("Stacking Model'in beklediği özellikler:", stacking_model.feature_names_in_.tolist())


# stacking_model, one hot encoding ve standardscaler işlemlerini .pickle ile kaydetme (bunları kullanacağım)  (a klasörüne kaydettim bu adı düzenleyelim..!)
joblib.dump(stacking_model, 'stacking_model.pkl')
joblib.dump(ohe, 'ohe.pkl')
joblib.dump(ss_dict, 'standard_scalers.pkl')

# scale edilmiş (ölçeklendirilmiş) sütun adları -> (kontrol amaçlı)
print("Ölçeklendirilmiş sütunlar:", list(ss_dict.keys()))