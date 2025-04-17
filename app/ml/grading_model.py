import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from typing import List, Dict, Union, Tuple

class AutoGradingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.model_path = "app/ml/models/grading_model.joblib"
        self.vectorizer_path = "app/ml/models/vectorizer.joblib"

    def preprocess_data(self, answers: List[str], correct_answers: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess the text data for training or prediction."""
        # Create features by comparing student answers with correct answers
        features = []
        for answer, correct in zip(answers, correct_answers):
            feature = {
                'length_ratio': len(answer) / len(correct),
                'common_words': len(set(answer.lower().split()) & set(correct.lower().split())),
                'answer_text': answer
            }
            features.append(feature)

        # Convert text to TF-IDF features
        text_features = self.vectorizer.fit_transform([f['answer_text'] for f in features])
        
        # Combine with other features
        additional_features = np.array([[f['length_ratio'], f['common_words']] for f in features])
        X = np.hstack((text_features.toarray(), additional_features))
        
        return X

    def train(self, training_data: List[Dict[str, Union[str, int]]]) -> Dict[str, float]:
        """Train the model with sample data."""
        # Extract answers and grades from training data
        answers = [item['answer'] for item in training_data]
        correct_answers = [item['correct_answer'] for item in training_data]
        grades = [item['grade'] for item in training_data]

        # Preprocess data
        X = self.preprocess_data(answers, correct_answers)
        y = np.array(grades)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        # Save model and vectorizer
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)

        return {
            'accuracy': accuracy,
            'report': report
        }

    def predict(self, answer: str, correct_answer: str) -> Dict[str, Union[int, float]]:
        """Predict the grade for a given answer."""
        if not self.is_trained:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_trained = True
            else:
                raise ValueError("Model not trained yet!")

        # Preprocess single answer
        X = self.preprocess_data([answer], [correct_answer])
        
        # Make prediction
        grade = self.model.predict(X)[0]
        confidence = np.max(self.model.predict_proba(X)[0])

        return {
            'predicted_grade': int(grade),
            'confidence': float(confidence)
        }

    def generate_sample_data(self, n_samples: int = 100) -> List[Dict[str, Union[str, int]]]:
        """Generate sample training data."""
        correct_answers = [
            "The mitochondria is the powerhouse of the cell.",
            "Python is a high-level programming language.",
            "Photosynthesis converts light energy into chemical energy."
        ]
        
        variations = {
            0: ["wrong answer", "completely incorrect", "unrelated response"],
            1: ["mitochondria creates energy", "python programming", "plants use sunlight"],
            2: ["mitochondria produces cell energy", "python is programming language", "photosynthesis uses light"],
            3: ["The mitochondria produces energy for cells", "Python is a programming language", "Photosynthesis converts sunlight to energy"]
        }

        data = []
        for _ in range(n_samples):
            correct_idx = np.random.randint(0, len(correct_answers))
            grade = np.random.randint(0, 4)
            
            answer = np.random.choice(variations[grade])
            if grade == 3:  # Sometimes use exact correct answer for grade 3
                answer = correct_answers[correct_idx]

            data.append({
                'answer': answer,
                'correct_answer': correct_answers[correct_idx],
                'grade': grade
            })

        return data

# Example usage
if __name__ == "__main__":
    # Initialize model
    grading_model = AutoGradingModel()
    
    # Generate and train with sample data
    sample_data = grading_model.generate_sample_data(100)
    training_results = grading_model.train(sample_data)
    
    # Make a prediction
    prediction = grading_model.predict(
        "The mitochondria produces energy for the cell",
        "The mitochondria is the powerhouse of the cell."
    )
    
    print(f"Training Results: {training_results}")
    print(f"Prediction: {prediction}") 