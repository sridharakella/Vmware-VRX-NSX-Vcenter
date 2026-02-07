from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

iris = load_iris()
X, y = iris.data, iris.target

clf = RandomForestClassifier(n_estimators=10)
clf.fit(X, y)

joblib.dump(clf, "model.pkl")
print("Model trained and saved as model.pkl")
