# Data preprocessing and model training
X_train_scaled = scaler.fit_transform(X_train_transformed)
X_test_scaled = scaler.transform(X_test_transformed)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Plot accuracy graph
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Predictions for train and test sets
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)

# Calculate R² scores for train and test sets
train_accuracy = r2_score(y_train, y_train_pred)
test_accuracy = r2_score(y_test, y_test_pred)

# Prepare data for plotting
accuracy = [train_accuracy, test_accuracy]
labels = ['Train Accuracy', 'Test Accuracy']

# Plot the accuracy
plt.figure(figsize=(8, 5))
plt.bar(labels, accuracy, color=['blue', 'green'])
plt.ylim(0, 1)  # R² score range
plt.title('Model Accuracy')
plt.ylabel('R² Score')
plt.xlabel('Dataset')
plt.text(0, train_accuracy, f"{train_accuracy:.2f}", ha='center', va='bottom')
plt.text(1, test_accuracy, f"{test_accuracy:.2f}", ha='center', va='bottom')
plt.show()