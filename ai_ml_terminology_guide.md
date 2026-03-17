# 🤖 AI & Machine Learning Terminology Guide (Interview Edition)

A comprehensive, interview-focused reference of essential AI/ML concepts with Python examples.

---

## 📌 How to Use This Guide

Each term includes:
- ✅ Interview Definition (what to say)
- 🧠 Key Insight (what interviewers expect you to understand)
- 🧑‍💻 Python Example (practical usage)

---

## 1. 🧠 Fundamentals

### Artificial Intelligence (AI)
- ✅ **Definition**: The field of building systems capable of performing tasks requiring human intelligence.
- 🧠 **Insight**: ML is a subset of AI.

---

### Machine Learning (ML)
- ✅ **Definition**: Algorithms that learn patterns from data instead of being explicitly programmed.
- 🧠 **Insight**: Core idea = learning mapping from input → output.

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
```

---

### Model
- ✅ **Definition**: A trained mathematical function that makes predictions.
- 🧠 **Insight**: Model = learned parameters + structure.

---

## 2. 📊 Types of Learning

### Supervised Learning
- ✅ Learns from labeled data.
- 🧠 Used for classification & regression.

```python
X, y = [[1], [2], [3]], [2, 4, 6]
model.fit(X, y)
```

---

### Unsupervised Learning
- ✅ Finds patterns in unlabeled data.
- 🧠 Used for clustering, dimensionality reduction.

```python
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2).fit(X)
```

---

### Reinforcement Learning
- ✅ Learns via rewards/penalties.
- 🧠 Used in robotics, gaming.

---

## 3. 📦 Data & Features

### Feature
- ✅ Input variable.
- 🧠 Quality of features > model complexity.

---

### Train/Test Split
- ✅ Splitting data to evaluate model performance.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)
```

---

## 4. ⚙️ Models & Algorithms

### Linear Regression
- ✅ Predicts continuous values.
- 🧠 Assumes linear relationship.

```python
model = LinearRegression().fit(X, y)
```

---

### Logistic Regression
- ✅ Used for classification.
- 🧠 Outputs probability using sigmoid.

```python
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression().fit(X, y)
```

---

### Decision Tree
- ✅ Tree-based decisions.
- 🧠 Easy to interpret but can overfit.

---

### Random Forest
- ✅ Ensemble of trees.
- 🧠 Reduces overfitting.

---

## 5. 🏋️ Training Concepts

### Overfitting
- ✅ Model memorizes training data.
- 🧠 High train accuracy, low test accuracy.

---

### Underfitting
- ✅ Model too simple.

---

### Learning Rate
- ✅ Step size during optimization.
- 🧠 Too high → unstable, too low → slow.

---

## 6. 📏 Evaluation Metrics

### Accuracy
```python
from sklearn.metrics import accuracy_score
accuracy_score(y_test, model.predict(X_test))
```

### Precision / Recall
- 🧠 Important in imbalanced datasets.

---

### F1 Score
- 🧠 Balance between precision & recall.

---

## 7. 🧬 Deep Learning

### Neural Network
- ✅ Layers of neurons.
- 🧠 Learns complex patterns.

```python
import torch.nn as nn
model = nn.Linear(10, 1)
```

---

### Activation Function
- ✅ Adds non-linearity.

---

### Backpropagation
- ✅ Updates weights using gradients.

---

## 8. 💬 NLP

### Tokenization
```python
text.split()
```

---

### Embeddings
- 🧠 Words → vectors.

---

## 9. 🚀 MLOps & Deployment

### Inference
- ✅ Using trained model.

```python
model.predict([[5]])
```

---

### Data Drift
- 🧠 Production data ≠ training data.

---

## 10. 🧪 Advanced Concepts

### Bias-Variance Tradeoff
- 🧠 Balance underfitting vs overfitting.

---

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score
cross_val_score(model, X, y, cv=5)
```

---

### Hyperparameter Tuning
```python
from sklearn.model_selection import GridSearchCV
GridSearchCV(model, param_grid={"fit_intercept": [True, False]})
```

---

## 🎯 Common Interview Questions

- What is overfitting and how do you prevent it?
- Difference between precision and recall?
- Why use cross-validation?
- When to use Random Forest vs Logistic Regression?
- Explain bias-variance tradeoff.

---

## 📎 Contribution

PRs welcome with better examples, diagrams, or questions.

## 📜 License

MIT License

---

⭐ Star the repo if this helped your interview prep!

