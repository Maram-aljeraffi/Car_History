# ==========================================
# Car History - Dashboard (Final Version)
# بالخطوط الكبيرة والألوان المريحة
# + Condition & Accident + Price Adjustment
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ==========================================
# Page Config
# ==========================================
st.set_page_config(
    page_title="Car History | تحليل أسعار السيارات",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Custom CSS - خطوط كبيرة + ألوان مريحة
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        font-size: 18px !important;
    }
    
    .stApp * {
        font-family: 'Cairo', sans-serif !important;
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stText, p, span, div {
        font-size: 1.2rem !important;
        line-height: 1.7 !important;
    }
    
    h1 { font-size: 3.5rem !important; font-weight: 800 !important; }
    h2 { font-size: 2.8rem !important; font-weight: 800 !important; }
    h3 { font-size: 2.2rem !important; font-weight: 700 !important; }
    h4 { font-size: 1.8rem !important; font-weight: 700 !important; }
    
    .stSelectbox label,
    .stTextInput label,
    .stNumberInput label,
    .stSlider label,
    label {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #2C3E50 !important;
    }
    
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        font-size: 1.3rem !important;
        padding: 0.9rem 1rem !important;
        border-radius: 10px !important;
        border: 1.5px solid #E8EEF4 !important;
    }
    
    .stButton > button {
        font-size: 1.4rem !important;
        padding: 1.1rem 2rem !important;
        font-weight: 700 !important;
        background: #3B6EA5 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #2E5A8A !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(59,110,165,0.3);
    }
    
    .stDataFrame, .stDataFrame * {
        font-size: 1.15rem !important;
    }
    
    [data-testid="stSidebar"] * {
        font-size: 1.25rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        font-size: 1.3rem !important;
        padding: 1.1rem 1.5rem !important;
        font-weight: 600 !important;
    }
    
    .main {
        background: #F7F9FC;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E8EEF4;
    }
    
    [data-testid="stSidebar"] * {
        color: #2C3E50 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        border-radius: 10px;
        margin: 0.25rem 0.75rem;
        transition: all 0.25s ease;
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: #F0F5FA;
    }
    
    .logo-block {
        padding: 2rem 1.5rem;
        text-align: center;
        border-bottom: 1px solid #E8EEF4;
    }
    
    .logo-mark {
        width: 80px;
        height: 80px;
        background: #3B6EA5;
        border-radius: 22px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(59,110,165,0.25);
    }
    
    .logo-name {
        font-size: 2rem !important;
        color: #2C3E50 !important;
        font-weight: 800;
        margin: 0;
    }
    
    .logo-tagline {
        font-size: 1.1rem !important;
        color: #7B8A9B !important;
        margin-top: 0.35rem;
        font-weight: 500;
    }
    
    .hero {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F5FA 100%);
        padding: 3.5rem;
        border-radius: 24px;
        margin-bottom: 2.5rem;
        border: 1px solid #E8EEF4;
        position: relative;
        overflow: hidden;
    }
    
    .hero::after {
        content: '🚗';
        position: absolute;
        top: 50%;
        left: 3rem;
        transform: translateY(-50%);
        font-size: 15rem;
        opacity: 0.06;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-eyebrow {
        font-size: 1.15rem !important;
        color: #3B6EA5;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }
    
    .hero h1 {
        color: #2C3E50;
        margin: 0;
        line-height: 1.15;
    }
    
    .hero p {
        color: #6B7A8D;
        margin-top: 1.25rem;
        font-weight: 400;
        line-height: 1.8;
        max-width: 800px;
        font-size: 1.35rem !important;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2.5rem;
    }
    
    .metric {
        background: #FFFFFF;
        padding: 2.25rem 2rem;
        border-radius: 20px;
        border: 1px solid #E8EEF4;
        transition: all 0.3s ease;
    }
    
    .metric:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(59,110,165,0.12);
        border-color: #D6E4F0;
    }
    
    .metric-icon {
        width: 60px;
        height: 60px;
        background: #F0F5FA;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-label {
        font-size: 1.15rem !important;
        color: #7B8A9B;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 2.8rem !important;
        font-weight: 800;
        color: #2C3E50;
        line-height: 1;
    }
    
    .metric-unit {
        font-size: 1.05rem !important;
        color: #A0AEBF;
        margin-top: 0.75rem;
        font-weight: 500;
    }
    
    .section-title {
        font-size: 2.3rem !important;
        font-weight: 800;
        color: #2C3E50;
        margin: 3rem 0 1.75rem 0;
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }
    
    .section-title::before {
        content: '';
        width: 6px;
        height: 42px;
        background: #3B6EA5;
        border-radius: 3px;
    }
    
    .result-price {
        background: linear-gradient(135deg, #3B6EA5 0%, #5A8FC7 100%);
        padding: 3.5rem 2rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        box-shadow: 0 20px 45px rgba(59,110,165,0.3);
    }
    
    .result-price .label {
        font-size: 1.25rem !important;
        opacity: 0.95;
        font-weight: 600;
        margin-bottom: 1.25rem;
    }
    
    .result-price .amount {
        font-size: 4.5rem !important;
        font-weight: 900;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .result-price .currency {
        font-size: 1.4rem !important;
        opacity: 0.9;
        font-weight: 600;
    }
    
    .result-category {
        background: #FFFFFF;
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid #D6E4F0;
        text-align: center;
        margin-top: 1rem;
    }
    
    .result-category .label {
        font-size: 1.2rem !important;
        color: #7B8A9B;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .result-category .value {
        font-size: 3rem !important;
        font-weight: 800;
        color: #3B6EA5;
    }
    
    .empty-state {
        background: #FFFFFF;
        border: 2px dashed #D6E4F0;
        padding: 5rem 2rem;
        border-radius: 20px;
        text-align: center;
    }
    
    .empty-state .icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .empty-state .text {
        color: #7B8A9B;
        font-size: 1.35rem !important;
        font-weight: 600;
    }
    
    .side-stat-box {
        padding: 1.5rem;
        margin: 0.75rem;
        background: #F7F9FC;
        border-radius: 14px;
        text-align: center;
    }
    
    .side-stat-label {
        font-size: 1.05rem !important;
        color: #7B8A9B;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .side-stat-value {
        font-size: 2rem !important;
        color: #3B6EA5;
        font-weight: 800;
    }
    
    .about-card {
        background: #FFFFFF;
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid #E8EEF4;
        height: 100%;
    }
    
    .about-card .label {
        font-size: 1.1rem !important;
        color: #7B8A9B;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .about-card .title {
        font-size: 1.9rem !important;
        color: #2C3E50;
        font-weight: 800;
        margin-bottom: 1.25rem;
    }
    
    .about-card ul {
        color: #6B7A8D;
        line-height: 2.2;
        font-size: 1.3rem !important;
        padding-right: 1.5rem;
    }
    
    .about-card .value {
        font-size: 2.5rem !important;
        color: #3B6EA5;
        font-weight: 800;
    }
    
    .tech-item {
        text-align: center;
        padding: 2rem 1.25rem;
        background: #FFFFFF;
        border: 1px solid #E8EEF4;
        border-radius: 20px;
        transition: all 0.3s;
    }
    
    .tech-item:hover {
        border-color: #3B6EA5;
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(59,110,165,0.12);
    }
    
    .tech-item .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .tech-item .name {
        font-weight: 700;
        color: #2C3E50;
        font-size: 1.3rem !important;
    }
    
    .footer {
        text-align: center;
        padding: 3rem 0 1rem 0;
        color: #A0AEBF;
        font-size: 1.15rem !important;
        font-weight: 500;
        border-top: 1px solid #E8EEF4;
        margin-top: 4rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Load Models & Data
# ==========================================
@st.cache_resource
def load_models():
    reg_model = joblib.load('models/regression_model_final.pkl')
    clf_model = joblib.load('models/classification_model_final.pkl')
    encoders = joblib.load('models/encoders_final.pkl')
    features = joblib.load('models/features_final.pkl')
    return reg_model, clf_model, encoders, features

@st.cache_data
def load_data():
    df = pd.read_csv('data/car_data_processed.csv')
    return df

reg_model, clf_model, encoders, features = load_models()
df = load_data()

# ==========================================
# Sidebar (تقتصر الآن على التنقل والإحصائيات الثابتة)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class='logo-block'>
        <div class='logo-mark'>🚗</div>
        <div class='logo-name'>Car History</div>
        <div class='logo-tagline'>تحليل أسعار السيارات</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    page = st.radio(
        "القائمة",
        ["📊 لوحة المعلومات", "🔮 التنبؤ بالسعر", "📈 الإحصائيات", "ℹ️ عن المشروع"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='padding: 0 1.5rem; font-size: 1.05rem; color: #7B8A9B; font-weight: 700; margin-bottom: 0.5rem;'>
        أداء النماذج
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='side-stat-box'>
        <div class='side-stat-label'>دقة الانحدار (R²)</div>
        <div class='side-stat-value'>0.9411</div>
    </div>
    <div class='side-stat-box'>
        <div class='side-stat-label'>دقة التصنيف</div>
        <div class='side-stat-value'>96%</div>
    </div>
    <div class='side-stat-box'>
        <div class='side-stat-label'>عدد السيارات</div>
        <div class='side-stat-value'>9,179</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# Page 1: Dashboard
# ==========================================
if page == "📊 لوحة المعلومات":
    
    st.markdown("""
    <div class='hero'>
        <div class='hero-content'>
            <div class='hero-eyebrow'>✨ منصة التحليل الذكي</div>
            <h1>تحليل أسعار السيارات</h1>
            <p>منصة متكاملة لتقييم السيارات المستعملة باستخدام الذكاء الاصطناعي، تمنحك رؤية واضحة ودقيقة للسوق</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-grid'>
        <div class='metric'>
            <div class='metric-icon'>💰</div>
            <div class='metric-label'>متوسط السعر</div>
            <div class='metric-value'>{df['Price_SAR'].mean():,.0f}</div>
            <div class='metric-unit'>ريال سعودي</div>
        </div>
        <div class='metric'>
            <div class='metric-icon'>🚗</div>
            <div class='metric-label'>عدد السيارات</div>
            <div class='metric-value'>{len(df):,}</div>
            <div class='metric-unit'>سيارة مسجلة</div>
        </div>
        <div class='metric'>
            <div class='metric-icon'>📅</div>
            <div class='metric-label'>متوسط السنة</div>
            <div class='metric-value'>{df['Year'].mean():.0f}</div>
            <div class='metric-unit'>سنة الصنع</div>
        </div>
        <div class='metric'>
            <div class='metric-icon'>🛣️</div>
            <div class='metric-label'>متوسط الكيلومترات</div>
            <div class='metric-value'>{df["KM's driven"].mean():,.0f}</div>
            <div class='metric-unit'>كيلومتر</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-title'>توزيع الفئات السعرية</div>", unsafe_allow_html=True)
        cat_counts = df['Price_Category'].value_counts()
        fig = px.pie(
            values=cat_counts.values,
            names=cat_counts.index,
            color_discrete_sequence=['#3B6EA5', '#7BA8D1', '#B8D0E5'],
            hole=0.55
        )
        fig.update_traces(
            textposition='outside',
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=3)),
            textfont=dict(size=16, family='Cairo', color='#2C3E50')
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=50, l=50, r=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<div class='section-title'>أكثر 10 ماركات</div>", unsafe_allow_html=True)
        top_makes = df['Make'].value_counts().head(10)
        fig = px.bar(
            x=top_makes.values,
            y=top_makes.index,
            orientation='h',
            color=top_makes.values,
            color_continuous_scale=['#D6E4F0', '#7BA8D1', '#3B6EA5']
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="",
            font=dict(size=15, family='Cairo', color='#2C3E50'),
            xaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
            yaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=15)),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        fig.update_traces(marker_line_color='white', marker_line_width=1)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-title'>متوسط السعر حسب سنة الصنع</div>", unsafe_allow_html=True)
    yearly_price = df.groupby('Year')['Price_SAR'].mean().reset_index()
    fig = px.area(
        yearly_price,
        x='Year',
        y='Price_SAR'
    )
    fig.update_traces(
        line_color='#3B6EA5',
        line_width=3,
        fillcolor='rgba(59,110,165,0.15)'
    )
    fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="سنة الصنع",
        yaxis_title="متوسط السعر (SAR)",
        font=dict(size=15, family='Cairo', color='#2C3E50'),
        xaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
        yaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Page 2: Prediction (تم نقل المدخلات إلى الصفحة الرئيسية مباشرة لتظهر على الجوال)
# ==========================================
elif page == "🔮 التنبؤ بالسعر":
    
    st.markdown("""
    <div class='hero'>
        <div class='hero-content'>
            <div class='hero-eyebrow'>🔮 تقدير دقيق</div>
            <h1>التنبؤ بسعر السيارة</h1>
            <p>أدخل مواصفات السيارة للحصول على تقدير دقيق للسعر العادل</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='section-title'>مواصفات السيارة</div>", unsafe_allow_html=True)
        
        # استخدام st بدلاً من st.sidebar لتظهر بوضوح في الصفحة الرئيسية
        make = st.selectbox("الماركة (Make)", options=df['Make'].unique()[:20])
        model = st.text_input("الموديل (Model)", value="Corolla")
        year = st.slider("سنة الصنع (Year)", 1990, 2024, 2020)
        km = st.number_input("الكيلومترات (KM's driven)", 0, 500000, 50000, step=5000)
        fuel = st.selectbox("نوع الوقود (Fuel)", options=df['Fuel'].unique())
        transmission = st.selectbox("ناقل الحركة (Transmission)", options=df['Transmission'].unique())
        
        condition = st.selectbox(
            "حالة السيارة (Condition)",
            options=['Used', 'Like New', 'New']
        )
        accident = st.selectbox(
            "سجل الحوادث (Accident)",
            options=['No', 'Yes']
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🔮 احسب السعر المتوقع", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("<div class='section-title'>النتيجة</div>", unsafe_allow_html=True)
        
        if predict_btn:
            condition_map = {'Used': 0, 'Like New': 1, 'New': 2}
            accident_map = {'No': 0, 'Yes': 1}
            
            input_data = pd.DataFrame({
                'Make': [make],
                'Model': [model],
                'Year': [year],
                "KM's driven": [km],
                'Fuel': [fuel],
                'Transmission': [transmission],
                'Condition': [condition_map[condition]],
                'Accident': [accident_map[accident]]
            })
            
            for col in features:
                if col in encoders:
                    try:
                        input_data[col] = encoders[col].transform(input_data[col].astype(str))
                    except:
                        input_data[col] = 0
            
            # التنبؤ الأساسي
            predicted_price = reg_model.predict(input_data)[0]
            predicted_category = clf_model.predict(input_data)[0]
            
            # ============================================
            # تعديل السعر يدوياً حسب Condition و Accident
            # ============================================
            base_price = predicted_price
            adjustment_reason = []
            
            if condition == 'New':
                predicted_price *= 1.15
                adjustment_reason.append("سيارة جديدة (+15%)")
            elif condition == 'Like New':
                predicted_price *= 1.07
                adjustment_reason.append("شبه جديدة (+7%)")
            
            if accident == 'Yes':
                predicted_price *= 0.82
                adjustment_reason.append("حادث (-18%)")
            
            # عرض السعر المتوقع
            st.markdown(f"""
            <div class='result-price'>
                <div class='label'>💰 السعر المتوقع</div>
                <div class='amount'>{predicted_price:,.0f}</div>
                <div class='currency'>ريال سعودي</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='result-category'>
                <div class='label'>🏷️ الفئة السعرية</div>
                <div class='value'>{predicted_category}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if adjustment_reason:
                st.info(f"💡 **تم تعديل السعر بناءً على:** {' و '.join(adjustment_reason)}")
                st.caption(f"السعر الأساسي قبل التعديل: {base_price:,.0f} SAR")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=predicted_price,
                number={'font': {'size': 44, 'color': '#2C3E50', 'family': 'Cairo'}, 'suffix': ' SAR'},
                gauge={
                    'axis': {
                        'range': [0, df['Price_SAR'].max()],
                        'tickwidth': 1,
                        'tickcolor': '#E8EEF4',
                        'tickfont': {'color': '#7B8A9B', 'size': 13}
                    },
                    'bar': {'color': "#3B6EA5", 'thickness': 0.3},
                    'bgcolor': "white",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, df['Price_SAR'].quantile(0.33)], 'color': "#F0F5FA"},
                        {'range': [df['Price_SAR'].quantile(0.33), df['Price_SAR'].quantile(0.66)], 'color': "#D6E4F0"},
                        {'range': [df['Price_SAR'].quantile(0.66), df['Price_SAR'].max()], 'color': "#B8D0E5"}
                    ],
                    'threshold': {
                        'line': {'color': "#4A9B7F", 'width': 4},
                        'thickness': 0.8,
                        'value': predicted_price
                    }
                }
            ))
            fig.update_layout(
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Cairo'),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='icon'>📋</div>
                <div class='text'>أدخل مواصفات السيارة ثم اضغط على زر التنبؤ</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# Page 3: Statistics
# ==========================================
elif page == "📈 الإحصائيات":
    
    st.markdown("""
    <div class='hero'>
        <div class='hero-content'>
            <div class='hero-eyebrow'>📈 رؤى البيانات</div>
            <h1>الإحصائيات التفصيلية</h1>
            <p>تحليل شامل واستكشاف عميق لبيانات السيارات</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>الإحصائيات الوصفية</div>", unsafe_allow_html=True)
    st.dataframe(
        df[['Price_SAR', 'Year', "KM's driven"]].describe().round(2),
        use_container_width=True
    )
    
    st.markdown("<div class='section-title'>توزيع الأسعار</div>", unsafe_allow_html=True)
    fig = px.histogram(
        df,
        x='Price_SAR',
        nbins=50,
        color_discrete_sequence=['#3B6EA5']
    )
    fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="السعر (SAR)",
        yaxis_title="",
        font=dict(size=15, family='Cairo', color='#2C3E50'),
        xaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
        yaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-title'>السعر حسب الفئة</div>", unsafe_allow_html=True)
        fig = px.box(
            df,
            x='Price_Category',
            y='Price_SAR',
            color='Price_Category',
            color_discrete_sequence=['#3B6EA5', '#7BA8D1', '#B8D0E5']
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=15, family='Cairo', color='#2C3E50'),
            xaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
            yaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("<div class='section-title'>السعر حسب الوقود</div>", unsafe_allow_html=True)
        fuel_price = df.groupby('Fuel')['Price_SAR'].mean().reset_index()
        fig = px.bar(
            fuel_price,
            x='Fuel',
            y='Price_SAR',
            color='Price_SAR',
            color_continuous_scale=['#D6E4F0', '#7BA8D1', '#3B6EA5']
        )
        fig.update_layout(
            height=450,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="",
            font=dict(size=15, family='Cairo', color='#2C3E50'),
            xaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=14)),
            yaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-title'>العلاقة بين الكيلومترات والسعر</div>", unsafe_allow_html=True)
    sample_df = df.sample(min(1000, len(df)))
    fig = px.scatter(
        sample_df,
        x="KM's driven",
        y='Price_SAR',
        color='Price_Category',
        hover_data=['Make', 'Model'],
        color_discrete_sequence=['#3B6EA5', '#7BA8D1', '#B8D0E5']
    )
    fig.update_layout(
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=15, family='Cairo', color='#2C3E50'),
        xaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
        yaxis=dict(gridcolor='#F0F5FA', zeroline=False, tickfont=dict(size=14)),
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14, family='Cairo'))
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Page 4: About
# ==========================================
else:
    
    st.markdown("""
    <div class='hero'>
        <div class='hero-content'>
            <div class='hero-eyebrow'>ℹ️ معلومات</div>
            <h1>عن المشروع</h1>
            <p>Car History - منصة تحليل أسعار السيارات</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='about-card'>
            <div class='label'>🎯 الهدف</div>
            <div class='title'>منصة ذكية للتقييم</div>
            <ul>
                <li>تقليل عدم الشفافية في أسعار السيارات</li>
                <li>مساعدة المشترين على اتخاذ قرارات مدروسة</li>
                <li>توفير تقدير عادل لسعر السيارة</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='about-card'>
            <div class='label'>📊 البيانات</div>
            <div class='title'>OLX Pakistan</div>
            <table style='width: 100%; margin-top: 0.5rem; color: #6B7A8D; font-size: 1.3rem;'>
                <tr><td style='padding: 0.9rem 0;'>عدد السيارات</td><td style='text-align: left; color: #2C3E50; font-weight: 700;'>9,179</td></tr>
                <tr><td style='padding: 0.9rem 0;'>الميزات</td><td style='text-align: left; color: #2C3E50; font-weight: 700;'>8 features</td></tr>
                <tr><td style='padding: 0.9rem 0;'>العملة</td><td style='text-align: left; color: #2C3E50; font-weight: 700;'>SAR</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='about-card'>
            <div class='label'>📈 نموذج الانحدار</div>
            <div class='title'>Random Forest Regressor</div>
            <div style='display: flex; justify-content: space-between; margin-top: 1.5rem; align-items: baseline;'>
                <span style='color: #7B8A9B; font-size: 1.2rem; font-weight: 600;'>دقة R²</span>
                <span class='value'>0.9411</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='about-card'>
            <div class='label'>🎯 نموذج التصنيف</div>
            <div class='title'>Random Forest Classifier</div>
            <div style='display: flex; justify-content: space-between; margin-top: 1.5rem; align-items: baseline;'>
                <span style='color: #7B8A9B; font-size: 1.2rem; font-weight: 600;'>الدقة</span>
                <span class='value'>96%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>التقنيات المستخدمة</div>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    techs = [("🐍", "Python"), ("📊", "Pandas"), ("🤖", "Scikit-learn"), ("📈", "Plotly")]
    for col, (icon, name) in zip(cols, techs):
        with col:
            st.markdown(f"""
            <div class='tech-item'>
                <div class='icon'>{icon}</div>
                <div class='name'>{name}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# Footer
# ==========================================
st.markdown("""
<div class='footer'>
    🚗 Car History © 2026 | Made:Maram_Aljeraffi  
</div>
""", unsafe_allow_html=True)