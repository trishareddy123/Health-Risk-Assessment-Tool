def validate_numeric_input(value, min_val, max_val):
    """Validate numeric input within specified range"""
    try:
        num_value = float(value)
        if min_val <= num_value <= max_val:
            return True
        return False
    except ValueError:
        return False

def get_risk_color(risk_level):
    """Return color code based on risk level"""
    colors = {
        0: "#28a745",  # Green for low risk
        1: "#ffc107",  # Yellow for medium risk
        2: "#dc3545"   # Red for high risk
    }
    return colors.get(risk_level, "#6c757d")

def get_risk_label(risk_level):
    """Return risk label based on risk level"""
    labels = {
        0: "Low Risk",
        1: "Medium Risk",
        2: "High Risk"
    }
    return labels.get(risk_level, "Unknown")

def generate_recommendations(features, risk_level):
    """Generate health recommendations based on features and risk level"""
    recommendations = []
    
    if features[0] > 30:  # BMI check
        recommendations.append("Consider consulting with a nutritionist for weight management advice.")
    
    if features[1] < 2:  # Exercise frequency
        recommendations.append("Aim for at least 150 minutes of moderate exercise per week.")
    
    if features[2] > 0:  # Smoking status
        recommendations.append("Consider smoking cessation programs - smoking significantly increases health risks.")
    
    if features[3] > 14:  # Alcohol consumption
        recommendations.append("Consider reducing alcohol intake to recommended levels.")
    
    if risk_level > 0:
        recommendations.append("Schedule regular check-ups with your healthcare provider.")
    
    return recommendations if recommendations else ["Maintain your current healthy lifestyle habits."]
