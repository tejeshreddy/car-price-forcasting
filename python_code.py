import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/car data.csv")
features = list(filter(lambda x: x!="Car_Name" ,list(df.columns)))

final_dataset = df[features]
final_dataset['No_Year'] = 2020 - df['Year']
final_dataset.drop(['Year'], axis=1, inplace=True)
final_dataset = pd.get_dummies(final_dataset, drop_first=True)

X = final_dataset.iloc[:, 1:]   # Independent features
y = final_dataset.iloc[:, 0]    # Dependent features

# Extrapolate the feature importance
from sklearn.ensemble import ExtraTreesRegressor
etr = ExtraTreesRegressor()
etr.fit(X, y)
print(dict(zip(list(X.columns) ,etr.feature_importances_)))

# Train test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.ensemble import RandomForestRegressor
rf_random = RandomForestRegressor()

# Hyperparameter tuning
n_estimators = [int(x) for x in np.linspace(start=100, stop=1200, num=12)]  # Number of tree in RF
max_features = ['auto', 'sqrt'] # Number of features to be considered for each split
max_depth = [int(x) for x in np.linspace(5, 30, num=6)] # Max number of leaves in each tree
min_samples_split = [2, 5, 10, 15, 100] # Minimum number of samples required to split a node
min_samples_leaf = [1, 2, 5, 10] # Minimum number of samples required at each leaf node

from sklearn.model_selection import RandomizedSearchCV

random_grid = {
    "n_estimators": n_estimators,
    "max_features": max_features,
    "max_depth": max_depth,
    "min_samples_split": min_samples_split,
    "min_samples_leaf": min_samples_leaf
}

# Init RandomizedSearchCV to find best tree
rf = RandomForestRegressor()
rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, scoring="neg_mean_squared_error",
                                n_iter=10, cv=5, verbose=2, random_state=42)

# Prediction for test set
predictions = rf_random.predict(X_test)

# Storing the model in a serialized file(pickle file)
import pickle
file = open('data/random_forest_regression_model.pkl', 'wb')
pickle.dump(rf_random, file) # To dump the data into the pickle file
