"""
Iris Classification Model Training Script

This script trains a Random Forest classifier on the classic Iris dataset
and saves the trained model to disk for later deployment in Kubernetes.

The Iris dataset contains 150 samples of iris flowers with 4 features each:
- Sepal length, sepal width, petal length, petal width
- 3 target classes: Setosa, Versicolor, Virginica

The trained model is serialized using joblib for efficient loading
in the Flask API serving endpoint (app.py).
"""

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the Iris dataset - a classic ML benchmark dataset
# X: feature matrix (150 samples x 4 features)
# y: target labels (0=Setosa, 1=Versicolor, 2=Virginica)
iris = load_iris()
X, y = iris.data, iris.target

# Initialize Random Forest classifier with 10 decision trees
# n_estimators=10 provides a good balance between accuracy and model size
# for this small dataset; production models typically use 100+ trees
clf = RandomForestClassifier(n_estimators=10)

# Train the model on the full dataset
# In production, you would split into train/test sets for validation
clf.fit(X, y)

# Serialize the trained model to disk using joblib
# joblib is preferred over pickle for sklearn models as it handles
# numpy arrays more efficiently (important for large models)
joblib.dump(clf, "model.pkl")
print("Model trained and saved as model.pkl")
