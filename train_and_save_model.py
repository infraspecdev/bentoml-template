from __future__ import annotations

import os
import pickle
import bentoml
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_and_save_model() -> None:
    # Load the Iris dataset
    logger.info("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target

    # Split the data into training and testing sets
    logger.info("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Initialize and train the KNeighborsClassifier model
    logger.info("Training KNeighborsClassifier model...")
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    # Evaluate the model
    logger.info("Evaluating the model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model accuracy: {accuracy:.2f}")

    # Save the model to a file
    model_file_path = "./models/iris.pickle"
    logger.info(f"Saving the model to {model_file_path}...")
    with open(model_file_path, "wb") as model_file:
        pickle.dump(model, model_file)
    logger.info("Model saved successfully.")

    # Save the model to BentoML model store
    bentoml_model = bentoml.picklable_model.save_model("iris_knn_model", model)
    logger.info(f"Model saved to BentoML model store with ID: {bentoml_model.id}")


if __name__ == "__main__":
    train_and_save_model()
