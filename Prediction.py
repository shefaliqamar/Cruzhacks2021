
# first neural network with keras tutorial
import numpy as np
import keras
from keras.models import Sequential, model_from_json
from keras.layers import Dense
import pandas as pd
import os

data = pd.read_json('https://cruzhacks2-default-rtdb.firebaseio.com/feedback.json')
data = data.transpose()


eth = [eth[0] for eth in data['ethnicity'].tolist()]
d = {'Ethnicity':eth}
df = pd.DataFrame(d)
data.drop(columns=['ethnicity'], inplace=True)
data['Ethnicity'] = pd.Series(df['Ethnicity'].to_numpy(), index=data.index)

# parse out side-effects + encode
ses = set([se for arr in data['symptoms'].tolist() for se in arr])
side_effects = {}
for se in ses:
    side_effects[se] = []
    for index, row in data.iterrows():
        if se in row['symptoms']:
            side_effects[se].append(1)
        else:
            side_effects[se].append(0)

for key in side_effects.keys():
    df = pd.DataFrame({key:side_effects[key]})
    data[key] = pd.Series(df[key].to_numpy(), index=data.index)


data = data.reset_index()
data.drop(columns=['index'], inplace=True)

print("Data: ", data.head(5))

X = data[['age', 'gender', 'Ethnicity']]
print("\n")
print(X)
print(X['age'].max())
print("\n")
y = data['Headache']

def one_hot_encoding(X, col):
    gen_dict = {gen:i for i,gen in enumerate(X[col].unique())} 
    # print("DICT: ", gen_dict)
    def integer_encode_gen(gen):
        return gen_dict[gen]
    X[col] = X[col].apply(integer_encode_gen)
    X = pd.concat([X,pd.get_dummies(X[col], prefix=col)],axis=1)
    X = X.drop(columns=[col])
    return X

def normalization(data, col):
    data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
    return data

X = one_hot_encoding(X, 'gender')
X = one_hot_encoding(X, 'Ethnicity')
X = X.astype({'age': 'float32'})
X = normalization(X, 'age')
X.dropna(axis=0, how='any', inplace=True)
print("\n")
print(X)
print(X.info())
print("\n")

def save_model(X, se):
    model = Sequential()
    model.add(Dense(12, input_dim=len(X.columns), activation='relu'))
    model.add(Dense(len(X.columns)/2, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X, y, epochs=150, batch_size=10)

    _, accuracy = model.evaluate(X, y)
    print(se, 'Accuracy: %.2f' % (accuracy*100))

    # # make probability predictions with the model
    # predictions = model.predict(X)
    # # round predictions 
    # rounded = [round(x[0]) for x in predictions]
    # print(predictions, rounded)
    # print(y.transpose())

    # serialize model to JSON
    model_json = model.to_json()
    with open(f"{se}_model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(f"{se}_model.h5")
    print("Saved model to disk")
    
def make_prediction(X, se):
    # load json and create model
    json_file = open(f'{se}_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(f"{se}_model.h5")
    print("Loaded model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    # score = loaded_model.evaluate(X, y, verbose=0)
    # print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
    predictions = loaded_model.predict(X)
    rounded = [round(x[0]) for x in predictions]
    return rounded 

# for se in ['Headache', 'Soreness', 'Swelling', 'Fever', 'Fatigue']:
#     save_model(X, se)

# print(X.head(1))
# print("Headache prediction: ", make_prediction(X.head(1), 'Headache'))

# for se in ['Pain at injection site', 'Chills']:
save_model(X, 'Chills')