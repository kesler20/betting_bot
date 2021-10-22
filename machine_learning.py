import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
import numpy as np
import pandas as pd
import sklearn
from sklearn import preprocessing as pp
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow.lite as tflite
import time
import random
from data_processing import DataProcessing

class NeuralNetwork:

    def __init__(self, number_of_labels, labels, data, processing):
        self.number_of_labels = number_of_labels
        self.labels = labels
        self.data = data
        self.processing = DataProcessing(self.data)

    def clean_data(self,filename):    
        p = pd.read_excel(filename)
        p = p.drop(['Unnamed: 0'], axis=1)
        p = p.drop(['time'], axis=1)
        X = np.array(p.drop(['Classes'], axis=1))
        Y = np.array(p['Classes'])
        train_labels, train_samples = shuffle(X,Y)
        return X, Y, p

    def initialize_model(self, X, Y):
        model = Sequential([
            Dense(units=len(self.data.columns), activation='relu'),
            Dense(units=32, activation='relu'),
            Dense(units=32, activation='relu'),
            Dense(units=self.number_of_labels, activation='softmax')
        ])

        X = np.asarray(X).astype('float32')
        model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy']) 

        model.fit(X, Y, epochs=30, shuffle=True, batch_size=30, use_multiprocessing=True, verbose=2)
        return model

    def save_best_model(self, x_data, y_data, repeats=15):
        model = self.initialize_model()
        best = (0, None)
        for n in range(repeats):
            x_train, x_test, y_train, y_test = train_test_split(x_data, y_data)
            model.fit(x_train, y_train, epochs=30, shuffle=True, batch_size=30, use_multiprocessing=True)
            acc = model.evaluate(x_data, y_data, use_multiprocessing=True)[1]
            if acc > best[0]:
                best = (acc, model)
        print(f'Best was {best[0] * 100}%')
        best[1].save('model2.tf')
        lite_model = tflite.TFLiteConverter.from_keras_model(best[1])
        open("model2.tflite", "wb").write(lite_model.convert())
        model = load_model(r'C:\Users\Uchek\OneDrive\Documents\Projects\learningpython\model2.tf')
        return model

    def iterate_predictions(self, model, X, Y, labels):
        while True:
            position = random.randint(0,len(X))
            n1 = X[position]
            n = self.processing.series_to_list(n1)
            h = []
            h.append(n)
            n = np.array(h, dtype='float32')
            prediction = model.predict(n)
            predicted_label = labels[np.argmax(prediction)]
            actual_label = labels[Y[position]]
            print(f"prediction : {predicted_label}, actual : {actual_label}")
            time.sleep(5)

