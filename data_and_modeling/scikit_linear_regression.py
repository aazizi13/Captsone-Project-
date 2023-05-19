import pickle
import pandas as pd
import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from joblib import dump, load  # More efficient pickle for numpy models

hdr = ['date', 'hour', 'origin', 'dest', 'trips']
dtypes = {'date': 'str', 'hour': int, 'origin': str, 'dest': str, 'trips': int}

df = pd.read_csv('date-hour-soo-dest-2022.csv',
        names=hdr,
        dtype=dtypes,
        parse_dates=['date'])

df['weekday'] = df['date'].dt.isocalendar().day
df['month'] = df['date'].dt.month
df['hour2'] = df['hour'] * df['hour']
df['hour3'] = df['hour'] * df['hour'] * df['hour']
df['trip'] = df['origin'] + '-' + df['dest']

#df['path'] = df['origin'] + '-' + df['dest']

X = df[['hour', 'weekday', 'month', 'origin', 'dest', 'hour2', 'hour3', 'trip']]
#, 'path']]  -- too computationally expensive.
Y = df['trips']

# Add categorical dummy variables.
X= pd.get_dummies(data=X) #, drop_first=True)

X = X[sorted(X.columns)]

with open('featurenames.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(X.columns, f, pickle.HIGHEST_PROTOCOL)

print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.5, random_state=101)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

model = LinearRegression()
model.fit(X_train, y_train)

dump(model, "linearmodel.joblib")

#coeff_parameter = pd.DataFrame(model.coef_,X.columns,columns=['Coefficient'])
#print(coeff_parameter)

#X_train_Sm= sm.add_constant(X_train)
#X_train_Sm= sm.add_constant(X_train)
#ls=sm.OLS(y_train,X_train_Sm).fit()
#print(ls.summary())

