import joblib
from sklearn.externals.array_api_compat.numpy import concat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline, Pipeline
from dataclasses import dataclass

@dataclass
class IntentResult:
    intent: str
    confidence: float

class Classifier:
    def __init__(self, path: str | None = None):
        self.pipeline = None
        if path:
            self.model = self.load(path)

    # Train the classifier on the given text and labels.
    # Vectorizes the text and fits a Naive Bayes classifier.
    def train(self, text: list[str], labels: list[str]):
        self.pipeline = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2)), 
            MultinomialNB()
        )
        
        self.pipeline = self.pipeline.fit(text, labels)

    def get_intent(self, text: str):
        if not self.model:
            raise ValueError("Model not loaded")
        
        probabilities = self.model.predict_proba([text])[0]
        max_idx = probabilities.argmax()
        confidence = float(probabilities[max_idx])
        intent = self.model.classes_[max_idx]

        if confidence < 0.1:
            return IntentResult(intent="UNKNOWN", confidence=confidence)

        return IntentResult(intent=intent, confidence=confidence)
    
    # Save the model to a file using joblib.
    def save(self, path: str):
        joblib.dump(self.pipeline, path)

    def load(self, path: str):
        return joblib.load(path)