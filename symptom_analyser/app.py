import os
import pandas as pd
import string
import pickle
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class Symptom_Analyser:
    def __init__(self):
        # Ensure the stopwords resource is available
        self.ensure_nltk_resources()

        # Initialize lemmatizer and stop words
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = stopwords.words('english') + list(string.punctuation)

        # Get the path to the dataset
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, 'symptom_data.csv')

        # Load the dataset
        data = pd.read_csv(data_path)

        # Preprocess symptoms
        data['Cleaned_Symptom'] = data['Symptom'].apply(self.clean_text)

        # Vectorize symptoms
        self.vectorizer = TfidfVectorizer(max_features=5000)
        X = self.vectorizer.fit_transform(data['Cleaned_Symptom'])

        # Labels (diseases)
        y = data['Disease']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate accuracy
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Model Accuracy: {accuracy * 100:.2f}%')

        # Save the trained model and vectorizer for future use
        with open(os.path.join(base_dir, 'rf_model.pkl'), 'wb') as model_file:
            pickle.dump(self.model, model_file)

        with open(os.path.join(base_dir, 'vectorizer.pkl'), 'wb') as vectorizer_file:
            pickle.dump(self.vectorizer, vectorizer_file)

    def ensure_nltk_resources(self):
        """
        Ensure that the required NLTK resources are available.
        """
        try:
            # Download stopwords resource if it's not already available
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    def clean_text(self, text):
        """
        Preprocess input text by removing stop words, punctuation, and lemmatizing.
        """
        words = word_tokenize(text.lower())
        return " ".join(
            self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words
        )

    def predict_disease(self, symptom):
        """
        Predict the disease based on input symptoms.
        """
        # Preprocess the symptom
        cleaned_symptom = self.clean_text(symptom)
        vectorized_symptom = self.vectorizer.transform([cleaned_symptom])

        # Predict disease
        predicted_disease = self.model.predict(vectorized_symptom)[0]
        return predicted_disease
