import json
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB
from fastapi_jwt_auth import AuthJWT

#Train model

# Load the data from JSON file
with open('chat/blog_qa.json') as json_file:
    data = json.load(json_file)

# Preprocess the data
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
for row in data:
    question = row['question']
    answer = row['answer']
    question_tokens = nltk.word_tokenize(question.lower())
    answer_tokens = nltk.word_tokenize(answer.lower())
    question_tokens = [lemmatizer.lemmatize(token) for token in question_tokens if token.isalnum() and token not in stop_words]
    answer_tokens = [lemmatizer.lemmatize(token) for token in answer_tokens if token.isalnum() and token not in stop_words]
    row['question_tokens'] = question_tokens
    row['answer_tokens'] = answer_tokens

# Create the feature matrix and target vector
questions = [' '.join(row['question_tokens']) for row in data]
answers = [row['answer'] for row in data]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)
y = answers

# Train the model
model = MultinomialNB()
model.fit(X, y)

# Evaluate the model
accuracy = model.score(X, y)
print('Model accuracy:', accuracy)

# Save the model
joblib.dump(model, 'chat/chat_model.joblib')

# Load the model
model = joblib.load('chat/chat_model.joblib')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


class PredictionResponse(BaseModel):
    answer: str
    
class PredictionRequest(BaseModel):
    question: str
    
router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post('/ask', response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    # Preprocess the input text (e.g., tokenize and vectorize)
    
    query = request.question.lower()
    query_tokens = nltk.word_tokenize(query.lower())
    query_tokens = [lemmatizer.lemmatize(token) for token in query_tokens if token.isalnum() and token not in stop_words]
    query = ' '.join(query_tokens)

    # Vectorize the query
    X_query = vectorizer.transform([query])

    # Make a prediction
    prediction = model.predict(X_query)

    # Return the prediction as a JSON response
    return PredictionResponse(answer=str(prediction[0]))