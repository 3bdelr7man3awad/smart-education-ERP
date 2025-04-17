import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from typing import List, Dict, Union, Tuple

class PerformancePredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = "app/ml/models/performance_model.joblib"
        self.scaler_path = "app/ml/models/performance_scaler.joblib"

    def preprocess_data(self, data: List[Dict[str, Union[float, int]]]) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess the student data for training or prediction."""
        df = pd.DataFrame(data)
        
        # Extract features and target
        features = ['attendance_rate', 'assignment_completion', 'quiz_average', 'study_hours']
        X = df[features].values
        y = df['performance_score'].values if 'performance_score' in df.columns else None
        
        # Scale features
        X = self.scaler.fit_transform(X)
        
        return X, y

    def train(self, training_data: List[Dict[str, Union[float, int]]]) -> Dict[str, float]:
        """Train the model with student performance data."""
        # Preprocess data
        X, y = self.preprocess_data(training_data)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model and scaler
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        return {
            'mean_squared_error': float(mse),
            'r2_score': float(r2)
        }

    def predict(self, student_data: Dict[str, Union[float, int]]) -> Dict[str, float]:
        """Predict student performance based on current metrics."""
        if not self.is_trained:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
            else:
                raise ValueError("Model not trained yet!")

        # Preprocess single student data
        X, _ = self.preprocess_data([student_data])
        
        # Make prediction
        predicted_score = self.model.predict(X)[0]
        
        return {
            'predicted_performance': float(predicted_score),
            'confidence_interval': {
                'lower': float(predicted_score - 5),  # Simplified confidence interval
                'upper': float(predicted_score + 5)
            }
        }

    def generate_sample_data(self, n_samples: int = 100) -> List[Dict[str, Union[float, int]]]:
        """Generate sample training data for student performance."""
        np.random.seed(42)
        
        data = []
        for _ in range(n_samples):
            # Generate realistic student metrics
            attendance = np.random.uniform(0.6, 1.0)  # 60-100% attendance
            assignments = np.random.uniform(0.5, 1.0)  # 50-100% completion
            quiz_avg = np.random.uniform(50, 100)  # 50-100 quiz average
            study_hours = np.random.uniform(1, 8)  # 1-8 hours per day
            
            # Calculate performance score with some noise
            base_score = (attendance * 25 + assignments * 25 + quiz_avg * 0.3 + study_hours * 2)
            noise = np.random.normal(0, 5)
            performance = min(100, max(0, base_score + noise))
            
            data.append({
                'attendance_rate': float(attendance),
                'assignment_completion': float(assignments),
                'quiz_average': float(quiz_avg),
                'study_hours': float(study_hours),
                'performance_score': float(performance)
            })
        
        return data

# Example usage
if __name__ == "__main__":
    # Initialize model
    predictor = PerformancePredictor()
    
    # Generate and train with sample data
    sample_data = predictor.generate_sample_data(100)
    training_results = predictor.train(sample_data)
    
    # Make a prediction for a student
    student_data = {
        'attendance_rate': 0.85,
        'assignment_completion': 0.9,
        'quiz_average': 85.0,
        'study_hours': 4.0
    }
    prediction = predictor.predict(student_data)
    
    print(f"Training Results: {training_results}")
    print(f"Prediction: {prediction}") 