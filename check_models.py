import joblib
import os

os.chdir('models')

model = joblib.load('regression_model_final.pkl')
encoders = joblib.load('encoders_final.pkl')
features = joblib.load('features_final.pkl')

print("=" * 50)
print("نوع النموذج:", type(model).__name__)
print("=" * 50)
print("الأعمدة المطلوبة:")
print(features)
print("=" * 50)
print("Encoders:")
if isinstance(encoders, dict):
    for k, v in encoders.items():
        print(f"  {k}: {type(v).__name__}")
else:
    print(type(encoders).__name__)
print("=" * 50)