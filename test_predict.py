import joblib
import os
import pandas as pd

os.chdir('models')
model = joblib.load('regression_model_final.pkl')
encoders = joblib.load('encoders_final.pkl')

# بيانات اختبار
data = pd.DataFrame([{
    'Make': 'Toyota',
    'Model': 'Yaris',
    'Year': 2015,
    "KM's driven": 100000,
    'Fuel': 'Petrol',
    'Transmission': 'Automatic',
    'Condition': 'Used',
    'Accident': 'No'
}])

# تشفير البيانات النصية (بالـ encoders)
for col in ['Make', 'Model', 'Fuel', 'Transmission']:
    data[col] = encoders[col].transform(data[col])

# تشفير Condition و Accident يدوياً
data['Condition'] = data['Condition'].map({'Used': 0, 'New': 1}).fillna(0).astype(int)
data['Accident'] = data['Accident'].map({'No': 0, 'Yes': 1}).fillna(0).astype(int)

# تأكدي إن كل البيانات رقمية
print("البيانات قبل التنبؤ:")
print(data)
print("أنواع البيانات:")
print(data.dtypes)

# التنبؤ
prediction = model.predict(data)[0]

print("=" * 40)
print("السعر المتوقع:", prediction)
print("=" * 40)