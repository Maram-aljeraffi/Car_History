from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

model = joblib.load(os.path.join(MODELS_DIR, 'regression_model_final.pkl'))
encoders = joblib.load(os.path.join(MODELS_DIR, 'encoders_final.pkl'))

print("=" * 50)
print("API Started Successfully")
print("=" * 50)

# ==========================================
# دالة ذكية للتعامل مع القيم النصية
# ==========================================
def smart_encode(encoder, value, default_value):
    """
    تحاول تشفير القيمة. إذا ما لقيتها، تبحث عنها بدون حساسية للأحرف.
    إذا فشلت، ترجع القيمة الافتراضية.
    """
    value_str = str(value).strip()
    
    # 1. المحاولة المباشرة (كما هي)
    try:
        return encoder.transform([value_str])[0]
    except ValueError:
        pass
    
    # 2. البحث بدون حساسية للأحرف (Case-Insensitive)
    for class_name in encoder.classes_:
        if str(class_name).lower() == value_str.lower():
            return encoder.transform([class_name])[0]
            
    # 3. إذا فشلت كل المحاولات، نرجع القيمة الافتراضية
    return encoder.transform([default_value])[0]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API is running'})


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        required = ['make', 'model', 'year', 'km_driven', 'fuel', 'transmission', 'condition', 'accident']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # ==========================================
        # التشفير الذكي (Smart Encoding)
        # ==========================================
        
        # الماركة: افتراضي Toyota
        make_encoded = smart_encode(encoders['Make'], data['make'], 'Toyota')
        
        # الموديل: افتراضي Corolla (لأنه أكثر موديل شائع)
        model_encoded = smart_encode(encoders['Model'], data['model'], 'Corolla GLI')
        
        # الوقود: افتراضي Petrol
        fuel_encoded = smart_encode(encoders['Fuel'], data['fuel'], 'Petrol')
        
        # ناقل الحركة: افتراضي Manual
        transmission_encoded = smart_encode(encoders['Transmission'], data['transmission'], 'Manual')
        
        # الحالة (Condition): 0=Used, 1=Like New, 2=New
        cond_str = str(data['condition']).lower()
        if cond_str == 'new':
            condition_encoded = 2
        elif cond_str == 'like new':
            condition_encoded = 1
        else:
            condition_encoded = 0
            
        # الحوادث (Accident): 0=No, 1=Yes
        accident_encoded = 1 if str(data['accident']).lower() == 'yes' else 0
        
        # ==========================================
        # بناء DataFrame والتنبؤ
        # ==========================================
        features = pd.DataFrame([{
            'Make': make_encoded,
            'Model': model_encoded,
            'Year': int(data['year']),
            "KM's driven": int(data['km_driven']),
            'Fuel': fuel_encoded,
            'Transmission': transmission_encoded,
            'Condition': condition_encoded,
            'Accident': accident_encoded
        }])
        
        prediction = float(model.predict(features)[0])
        
        return jsonify({
            'status': 'success',
            'predicted_price': round(prediction, 2),
            'currency': 'SAR'
        })
    
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)