# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EWmn4N4ZnrCSniQQNuOw7gyMtkrWkZz7
"""

import streamlit as st
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

@st.cache
def load_and_preprocess_data():
    # Load the dataset
    data = pd.read_csv('Heart.csv')

    # Identify categorical and numerical columns
    categorical_cols = ['cp', 'slope', 'thal']
    numerical_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

    # One-Hot Encoding
    encoder = OneHotEncoder(drop='first', sparse_output=False)
    encoded_features = pd.DataFrame(
        encoder.fit_transform(data[categorical_cols]),
        columns=encoder.get_feature_names_out(categorical_cols)
    )
    data = data.drop(categorical_cols, axis=1)
    data = pd.concat([data, encoded_features], axis=1)

    # Standard Scaling
    scaler = StandardScaler()
    data[numerical_cols] = scaler.fit_transform(data[numerical_cols])

    return data, scaler, encoder, numerical_cols

@st.cache
def train_model(data):
    # Define features and target
    X = data.drop('target', axis=1)
    y = data['target']

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Gradient Boosting Classifier
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    return model, X.columns

# Load data and train model
data, scaler, encoder, numerical_cols = load_and_preprocess_data()
model, feature_columns = train_model(data)

# Streamlit App UI
st.title("Heart Disease Prediction App")

st.sidebar.header("Input Features")
input_features = []
for col in feature_columns:
    if col in numerical_cols:
        val = st.sidebar.slider(f"{col}:", -3.0, 3.0, 0.0)
    else:
        val = st.sidebar.selectbox(f"{col}:", [0, 1], index=0)
    input_features.append(val)

if st.button("Predict"):
    input_df = pd.DataFrame([input_features], columns=feature_columns)
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

    prediction = model.predict(input_df)[0]
    result = "Heart Disease" if prediction == 1 else "No Heart Disease"

    st.subheader("Prediction Result:")
    st.write(f"The person is predicted to have **{result}**.")