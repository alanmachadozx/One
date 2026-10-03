import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class Classifier:

    # Train the classifier on the given text and labels.
    # Vectorizes the text and fits a Naive Bayes classifier.
    def train(self, text: list[str], labels: list[str]):
        model = make_pipeline(
            TfidfVectorizer(), 
            MultinomialNB()
        )
        
        model.fit(text, labels)
        return model
    
    # Save the model to a file using joblib.
    def save(self, model: object, path: str):
        joblib.dump(model, path)
        