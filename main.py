import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from model import create_model, predict_risk, get_feature_importance
from utils import validate_numeric_input, get_risk_color, get_risk_label, generate_recommendations

# Page configuration
st.set_page_config(
    page_title="Health Risk Assessment",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = create_model()

# Title and introduction
st.title("🏥 Health Risk Assessment Tool")
st.markdown("""
This tool uses artificial intelligence to assess your potential health risks based on
lifestyle factors and medical history. Please provide accurate information for the best results.

**Note:** This assessment is for informational purposes only and should not replace professional medical advice.
""")

# Privacy notice
with st.expander("📋 Privacy Notice"):
    st.markdown("""
    - All data is processed locally and is not stored or transmitted
    - No personal identification information is collected
    - This tool is for educational purposes only
    """)

# Create form for user input
with st.form("health_assessment_form"):
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bmi = st.number_input("BMI", 
                             min_value=15.0, 
                             max_value=50.0, 
                             value=25.0,
                             help="Body Mass Index (weight in kg / height in m²)")
        
        exercise_freq = st.slider("Exercise (hours/week)", 
                                min_value=0, 
                                max_value=20, 
                                value=3,
                                help="Average hours of moderate exercise per week")
        
        smoking = st.selectbox("Smoking Status",
                             options=["Never", "Former", "Current"],
                             help="Current smoking status")
        
        alcohol = st.number_input("Alcohol (drinks/week)",
                                min_value=0,
                                max_value=50,
                                value=2,
                                help="Average alcoholic drinks per week")
        
        sleep = st.slider("Sleep (hours/day)",
                         min_value=4,
                         max_value=12,
                         value=7,
                         help="Average hours of sleep per day")

    with col2:
        systolic_bp = st.number_input("Systolic Blood Pressure",
                                    min_value=90,
                                    max_value=200,
                                    value=120,
                                    help="Upper number of blood pressure reading")
        
        cholesterol = st.number_input("Total Cholesterol",
                                    min_value=100,
                                    max_value=300,
                                    value=180,
                                    help="Total cholesterol level in mg/dL")
        
        diabetes_family = st.checkbox("Family History of Diabetes",
                                    help="Immediate family members with diabetes")
        
        heart_disease_family = st.checkbox("Family History of Heart Disease",
                                         help="Immediate family members with heart disease")
        
        stress_level = st.slider("Stress Level",
                               min_value=1,
                               max_value=10,
                               value=5,
                               help="Subjective stress level (1-10)")

    submit_button = st.form_submit_button("Calculate Health Risk")

# Process form submission
if submit_button:
    # Prepare features
    features = [
        bmi,
        exercise_freq,
        {"Never": 0, "Former": 1, "Current": 2}[smoking],
        alcohol,
        sleep,
        systolic_bp,
        cholesterol,
        int(diabetes_family),
        int(heart_disease_family),
        stress_level
    ]
    
    # Get prediction
    risk_level, risk_probabilities = predict_risk(st.session_state.model, features)
    
    # Display results
    st.header("Assessment Results")
    
    # Risk level indicator
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_level,
            title={'text': "Risk Level"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 2], 'ticktext': ["Low", "Medium", "High"], 'tickvals': [0, 1, 2]},
                'steps': [
                    {'range': [0, 0.5], 'color': "#28a745"},
                    {'range': [0.5, 1.5], 'color': "#ffc107"},
                    {'range': [1.5, 2], 'color': "#dc3545"}
                ],
                'bar': {'color': get_risk_color(risk_level)}
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Risk probability breakdown
        labels = ['Low Risk', 'Medium Risk', 'High Risk']
        fig = px.bar(
            x=labels,
            y=risk_probabilities,
            title="Risk Probability Distribution",
            labels={'x': 'Risk Category', 'y': 'Probability'},
            color=labels,
            color_discrete_map={
                'Low Risk': "#28a745",
                'Medium Risk': "#ffc107",
                'High Risk': "#dc3545"
            }
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Recommendations
    st.subheader("Recommendations")
    recommendations = generate_recommendations(features, risk_level)
    for rec in recommendations:
        st.markdown(f"- {rec}")

    # Feature importance
    st.subheader("Risk Factors Analysis")
    feature_importance = get_feature_importance(st.session_state.model)
    feature_names = [
        "BMI", "Exercise", "Smoking", "Alcohol", "Sleep",
        "Blood Pressure", "Cholesterol", "Diabetes History",
        "Heart Disease History", "Stress"
    ]
    
    fig = px.bar(
        x=feature_names,
        y=feature_importance,
        title="Impact of Different Factors on Risk Assessment",
        labels={'x': 'Factor', 'y': 'Importance'},
        color=feature_importance,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Disclaimer: This tool provides general health risk assessment and should not be used as a substitute for professional medical advice.</small>
</div>
""", unsafe_allow_html=True)
