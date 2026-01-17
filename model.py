from sklearn.ensemble import RandomForestClassifier
import numpy as np

def create_model():
    """Create and return a pre-trained model for health risk assessment"""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Generate synthetic training data
    # In a real application, this would be replaced with actual training data
    np.random.seed(42)
    X = np.random.rand(1000, 10)  # 10 features
    # Create synthetic labels (0: low risk, 1: medium risk, 2: high risk)
    y = np.where(X.mean(axis=1) < 0.4, 0,
                 np.where(X.mean(axis=1) < 0.7, 1, 2))
    
    # Train the model
    model.fit(X, y)
    return model

def predict_risk(model, features):
    """Predict health risk based on input features"""
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    return prediction, probabilities

def get_feature_importance(model):
    """Get feature importance scores from the model"""
    return model.feature_importances_
