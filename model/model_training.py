import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, ShuffleSplit, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.tree import DecisionTreeRegressor
import pickle
import json

df = pd.read_csv("Data_cleaned.csv")

X = df.drop(['price'], axis='columns')
y = df['price']

# ============================================
# Linear Regression Model
# ============================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
lr_clf = LinearRegression()
lr_clf.fit(X_train, y_train)
#print("Linear Regression Test Score:", lr_clf.score(X_test, y_test))

# # ============================================
# # Cross Validation
# # ============================================
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
#print(cross_val_score(LinearRegression(), X, y, cv=cv))

# ============================================
# GridSearchCV for Best Model
# ============================================
def find_best_model_using_gridsearchcv(X, y):
    algos = {
        'linear_regression': {
            'model': LinearRegression(),
            'params': {'fit_intercept': [True, False]}
        },
        'lasso': {
            'model': Lasso(),
            'params': {'alpha': [1, 2], 'selection': ['random', 'cyclic']}
        },
        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {'criterion': ['squared_error'], 'splitter': ['best', 'random']}
        }
    }

    scores = []
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    for algo_name, config in algos.items():
        gs = GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
        gs.fit(X, y)
        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores, columns=['model', 'best_score', 'best_params'])

#print(find_best_model_using_gridsearchcv(X, y))


def predict_price(location, sqft, bath, bhk):
    loc_index = np.where(X.columns == location)[0][0]
    x = np.zeros(len(X.columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return lr_clf.predict([x])[0]

print(predict_price('1st Phase JP Nagar', 1000, 2, 2))
print(predict_price('Indira Nagar', 1000, 3, 3))


with open('bangalore_home_prices_model.pickle', 'wb') as f:
    pickle.dump(lr_clf, f)

columns = {'data_columns': [col.lower() for col in X.columns]}
with open("columns.json", "w") as f:
    f.write(json.dumps(columns))

print("Model training complete. Model and columns saved.")
