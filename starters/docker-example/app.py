from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train a simple Random Forest Classifier
clf = RandomForestClassifier(n_estimators=10)
clf.fit(X, y)

# Save the model
joblib.dump(clf, 'model.joblib')

# Create a Flask app
app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect data from form
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])
    
    # Make prediction
    features = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)
    prediction = model.predict(features)
    predicted_class = int(prediction[0])
    flower_names = ['Setosa', 'Versicolour', 'Virginica']
    predicted_name = flower_names[predicted_class]
    
    return jsonify({'prediction': f'Iris flower predicted: {predicted_name}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)