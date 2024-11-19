import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the Lemmatizer
lemmatizer = WordNetLemmatizer()

# Stopwords and punctuation to remove
stop_words = stopwords.words('english') + list(string.punctuation)

# Data loading and cleaning
def clean_text(text):
    """
    Function to clean the input text by tokenizing, removing stop words, punctuation,
    and lemmatizing the words.
    """
    words = word_tokenize(text.lower())  # Tokenize text into words
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Lemmatization and remove stopwords
    return " ".join(words)  # Join the cleaned words back to a string

# Load your dataset (ensure this path is correct)
data = pd.read_csv('symptom_data.csv')

# Clean the text (symptoms)
data['Cleaned_Symptom'] = data['Symptom'].apply(clean_text)

# Vectorize the symptoms using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)  # Limit to 5000 features
X = vectorizer.fit_transform(data['Cleaned_Symptom'])  # Transform symptoms to feature vectors

# The labels (Diseases)
y = data['Disease']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Initialize the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Save the model and vectorizer for future use
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# Function to predict disease from symptoms
def predict_disease(symptom):
    """
    Function to predict the disease based on symptoms input.
    It cleans and vectorizes the input symptom, then predicts the disease using the trained model.
    """
    # Clean and vectorize the symptom
    symptom_cleaned = clean_text(symptom)
    symptom_vectorized = vectorizer.transform([symptom_cleaned])
    
    # Load the trained model
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Predict and return the result
    predicted_disease = model.predict(symptom_vectorized)[0]
    return predicted_disease

# Example Usage
if __name__ == "__main__":
    # Example symptom input
    test_symptom =input("Symptoms:")
    predicted_disease = predict_disease(test_symptom)
    print(f"The predicted disease for the symptom '{test_symptom}' is: {predicted_disease}")
