# pcos_app_fixed.py
import streamlit as st
import numpy as np

# Simple configuration that definitely works
st.set_page_config(
    page_title="PCOS Risk Assessment",
    page_icon="🏥",
    layout="wide"
)

def main():
    # Custom CSS without complex theming
    st.markdown("""
    <style>
    .risk-high {
        background-color: #f8d7da;
        color: #721c24;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
    .risk-medium {
        background-color: #fff3cd;
        color: #856404;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .risk-low {
        background-color: #d4edda;
        color: #155724;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏥 PCOS Risk Assessment")
    st.markdown("### Complete this questionnaire to assess your risk of Polycystic Ovary Syndrome")
    
    # Sidebar for user input
    with st.sidebar:
        st.header("Patient Information")
        
        age = st.slider("Age", 15, 50, 25)
        
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", 100.0, 250.0, 160.0)
        with col2:
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 60.0)
        
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        st.info(f"**BMI:** {bmi:.1f}")
        
        col3, col4 = st.columns(2)
        with col3:
            waist = st.number_input("Waist (cm)", 50.0, 150.0, 70.0)
        with col4:
            hip = st.number_input("Hip (cm)", 60.0, 200.0, 90.0)
        
        # Calculate WHR
        if hip > 0:
            whr = waist / hip
            st.info(f"**Waist-to-Hip Ratio:** {whr:.2f}")
    
    # Main form
    st.header("Medical History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Menstrual Cycle")
        cycle_length = st.selectbox("Cycle Length", 
                                   ["Regular (21-35 days)", "Irregular (<21 or >35 days)"])
        period_length = st.slider("Period Duration (days)", 1, 10, 5)
    
    with col2:
        st.subheader("Lifestyle")
        sleep_hours = st.slider("Sleep Hours/Night", 3.0, 12.0, 7.0, 0.5)
        stress_level = st.slider("Stress Level", 1, 10, 5)
        exercise = st.selectbox("Exercise Frequency", 
                               ["Sedentary", "Light", "Moderate", "Active"])
    
    # Symptoms
    st.subheader("Symptoms")
    symptoms_col1, symptoms_col2 = st.columns(2)
    
    with symptoms_col1:
        acne = st.checkbox("Acne")
        hair_loss = st.checkbox("Hair Loss")
        hirsutism = st.checkbox("Excess Facial/Body Hair")
        skin_darkening = st.checkbox("Skin Darkening")
    
    with symptoms_col2:
        weight_gain = st.checkbox("Unexplained Weight Gain")
        fatigue = st.checkbox("Fatigue")
        mood_swings = st.checkbox("Mood Swings")
        sleep_issues = st.checkbox("Sleep Issues")
    
    # Optional Lab Results
    st.subheader("Optional Lab Results")
    lab_col1, lab_col2 = st.columns(2)
    
    with lab_col1:
        fsh = st.number_input("FSH (mIU/mL)", 0.0, 20.0, 0.0, 0.1)
        lh = st.number_input("LH (mIU/mL)", 0.0, 20.0, 0.0, 0.1)
    
    with lab_col2:
        if fsh > 0:
            fsh_lh_ratio = lh / fsh
            st.info(f"**FSH/LH Ratio:** {fsh_lh_ratio:.2f}")
        else:
            fsh_lh_ratio = 0.0
        
        amh = st.number_input("AMH (ng/mL)", 0.0, 20.0, 0.0, 0.1)
    
    # Calculate Risk Button
    if st.button("🎯 Calculate PCOS Risk", type="primary", use_container_width=True):
        # Calculate risk using enhanced algorithm
        risk_percentage = calculate_pcos_risk(
            age=age,
            bmi=bmi,
            whr=whr,
            cycle_length=cycle_length,
            period_length=period_length,
            sleep_hours=sleep_hours,
            stress_level=stress_level,
            exercise=exercise,
            acne=acne,
            hair_loss=hair_loss,
            hirsutism=hirsutism,
            skin_darkening=skin_darkening,
            weight_gain=weight_gain,
            fatigue=fatigue,
            mood_swings=mood_swings,
            sleep_issues=sleep_issues,
            fsh=fsh,
            lh=lh,
            fsh_lh_ratio=fsh_lh_ratio,
            amh=amh
        )
        
        # Display results
        display_results(risk_percentage)

def calculate_pcos_risk(age, bmi, whr, cycle_length, period_length, sleep_hours, 
                       stress_level, exercise, acne, hair_loss, hirsutism, 
                       skin_darkening, weight_gain, fatigue, mood_swings, 
                       sleep_issues, fsh, lh, fsh_lh_ratio, amh):
    """Calculate PCOS risk based on input parameters"""
    
    risk_score = 0
    
    # Age factor (18-35 highest risk)
    if 18 <= age <= 35:
        risk_score += 15
    
    # BMI factor
    if 25 <= bmi < 30:
        risk_score += 20
    elif bmi >= 30:
        risk_score += 30
    
    # Waist-to-hip ratio
    if whr > 0.85:
        risk_score += 15
    
    # Menstrual cycle
    if "Irregular" in cycle_length:
        risk_score += 25
    
    # Symptoms
    symptoms = [acne, hair_loss, hirsutism, skin_darkening, weight_gain, fatigue, mood_swings, sleep_issues]
    symptom_count = sum(symptoms)
    risk_score += symptom_count * 8
    
    # Extra weight for key symptoms
    if hirsutism:
        risk_score += 10
    if weight_gain:
        risk_score += 8
    
    # Lifestyle factors
    if sleep_hours < 6:
        risk_score += 8
    
    if stress_level >= 7:
        risk_score += 10
    
    exercise_risk = {"Sedentary": 12, "Light": 6, "Moderate": 3, "Active": 0}
    risk_score += exercise_risk.get(exercise, 0)
    
    # Lab results
    if fsh > 0 and lh > fsh:
        risk_score += 20
    
    if amh > 4.9:
        risk_score += 15
    
    return min(risk_score, 100)

def display_results(risk_percentage):
    """Display the risk assessment results"""
    
    st.markdown("---")
    st.markdown("## 📊 Assessment Results")
    
    # Risk percentage and progress bar
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"<h1 style='text-align: center; color: #8a2be2; font-size: 4rem;'>{risk_percentage:.1f}%</h1>", 
                    unsafe_allow_html=True)
        st.progress(int(risk_percentage))
    
    with col2:
        # Determine risk level
        if risk_percentage < 30:
            risk_level = "Low Risk"
            risk_class = "risk-low"
            recommendations = [
                "Maintain healthy lifestyle with balanced diet and exercise",
                "Continue monitoring menstrual cycle patterns",
                "Schedule regular check-ups with healthcare provider"
            ]
        elif risk_percentage < 60:
            risk_level = "Medium Risk"
            risk_class = "risk-medium"
            recommendations = [
                "Consult with healthcare provider for proper diagnosis",
                "Consider lifestyle modifications",
                "Monitor symptoms and keep records",
                "Consider hormone level tests"
            ]
        else:
            risk_level = "High Risk"
            risk_class = "risk-high"
            recommendations = [
                "Schedule appointment with healthcare provider ASAP",
                "Request comprehensive PCOS diagnostic tests",
                "Implement lifestyle changes focusing on weight management",
                "Consider consulting with endocrinologist or gynecologist"
            ]
        
        st.markdown(f"<div class='{risk_class}'><h3>{risk_level}</h3></div>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("### 📝 Recommendations")
    for rec in recommendations:
        st.write(f"• {rec}")
    
    # Risk interpretation
    st.markdown("### 🔍 Understanding Your Risk Score")
    risk_col1, risk_col2, risk_col3 = st.columns(3)
    
    with risk_col1:
        st.metric("Low Risk", "< 30%", "Minimal risk factors")
    
    with risk_col2:
        st.metric("Medium Risk", "30-60%", "Some risk factors present")
    
    with risk_col3:
        st.metric("High Risk", "> 60%", "Multiple risk factors")
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    ### ⚠️ Medical Disclaimer
    **This assessment is for informational purposes only and is not a substitute for professional medical advice. 
    Always consult with a qualified healthcare provider for proper diagnosis and treatment.**
    """)

if __name__ == "__main__":
    main()