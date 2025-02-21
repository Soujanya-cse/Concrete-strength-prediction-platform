import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# Load the dataset
data_path = "C:\\Users\\sowja\\OneDrive\\Desktop\\Concrete_Data.xlsx"
concrete = pd.read_excel(data_path)

# Rename columns for easier access
concrete.columns = ['cement', 'blastFurnace', 'flyAsh', 'water', 
                    'superplasticizer', 'courseAggregate', 'fineaggregate', 
                    'age', 'strength']

# Prepare features and target variable
X = concrete.drop("strength", axis=1)
y = concrete["strength"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply Power Transformation for normalization
pt = PowerTransformer(method='yeo-johnson')
X_train_transformed = pt.fit_transform(X_train)
X_test_transformed = pt.transform(X_test)

# Apply Standard Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_transformed)
X_test_scaled = scaler.transform(X_test_transformed)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
print("Model Performance:")
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Save the model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Save the transformers
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)
with open('power_transformer.pkl', 'wb') as file:
    pickle.dump(pt, file)

print("Model and transformers saved successfully.")
