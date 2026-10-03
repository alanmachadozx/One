import unittest
from src.classifier.model import * 

class TestClassifier(unittest.TestCase):
    def test_get_intent(self):
        classifier = Classifier("src/classifier/model.joblib")
        intent_object = classifier.get_intent("open")

        confidence = intent_object.confidence
        intent = intent_object.intent

        print(f"Intent: {intent}, Confidence: {confidence}")

if __name__ == '__main__':
    unittest.main()