# Machine Learning Intent Classifier

This document outlines the machine learning architecture used to understand and categorize user commands within the "One" project. The system relies on a custom Natural Language Processing (NLP) classification model defined in [model.py](../src/classifier/model.py) and trained via [trainer.py](../src/classifier/trainer.py).

## Model Architecture and Prediction

The core of the NLP engine is the `Classifier` class, which leverages the `scikit-learn` library to predict user intents from transcribed text. When initialized, the classifier constructs a machine learning pipeline consisting of two main stages: a `TfidfVectorizer` configured to extract unigrams and bigrams, followed by a `LogisticRegression` model that computes the final probabilities. 

When the main application receives a voice command, the text is passed to the `get_intent()` method. The model calculates the probability distribution across all known intents and selects the one with the highest score. To prevent the assistant from executing incorrect actions when it doesn't clearly understand a command, the system applies a strict confidence threshold (defaulting to 0.11). If the highest probability falls below this threshold, or if the input text is null, the classifier safely falls back to an `"UNKNOWN"` intent. 

Regardless of the outcome, the prediction is structured into an `IntentResult` data class, returning both the recognized intent string and the exact confidence float back to the execution pipeline. The class also includes utility methods to dynamically `save()` and `load()` the serialized pipeline model from disk.

## Dataset and Training Pipeline

Because the model needs to understand a variety of phrasing for the same action, it is trained on a structured JSON dataset [dataset.json](../src/classifier/dataset/dataset.json). This dataset acts as a dictionary mapping strict system intents (such as opening apps, controlling music playback, or asking the Gemini AI) to arrays of conversational examples that a user might naturally say. 

The model is not trained at runtime by the main application. Instead, it utilizes a standalone script, `trainer.py`, which handles the data ingestion and model generation. The script reads the JSON file, flattens the dictionary into a list of training texts and their corresponding labels, and feeds them into the classifier's `train` method. Once the logistic regression model is fully fitted to the dataset, it is serialized and exported as a `.joblib` artifact (`src/classifier/model.joblib`). This allows the main listener daemon to quickly load the pre-trained weights into memory without having to reprocess the dataset on every startup.