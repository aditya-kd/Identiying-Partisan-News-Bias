# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense ,Embedding, LSTM, SpatialDropout1D, Dropout
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical

SEED = 7                        # Fixes random seed for reproducibility.
URL = 'ibcData.csv'             # Specified dataset to gather data from.
SEPERATOR = ','                 # Seperator the dataset uses to divide data.
PADDING_LENGTH = 1000           # The amount of words allowed per piece of text.
HIDDEN_LAYER_SIZE = 300         # Details the amount of nodes in a hidden layer.
TOP_WORDS = 5000                # Most-used words in the dataset.
MAX_REVIEW_LENGTH = 500         # Char length of each text being sent in (necessary).
EMBEDDING_VECTOR_LENGTH = 112   # The specific Embedded later will have 112-length vectors to
                                # represent each word.
BATCH_SIZE = 32                 # Takes 32 sentences at a time and continually retrains RNN.
NUMBER_OF_EPOCHS = 100          # Fits RNN to more accurately guess the data's political bias.
VERBOSE = 1                     # Gives a lot of information when predicting/evaluating model.
NONVERBOSE = 0                  # Gives only results when predicting/evaluating model.
VALIDATION_SIZE = 1000          # The size that you want your validation sets to be.
DROPOUT = 0.2                   # Helps slow down overfitting of data (slower convergence rate)
FILE_NAME = 'finalizedModel.h5'


def debugAfterCleanUp(data):
    print(data)
    print(data[ data['bias'] == 'Conservative'].size)
    print(data[ data['bias'] == 'Liberal'].size)

# Checks the shape of the below four datasets
def checkShapes(X_train, X_test, Y_train, Y_test):
    print(X_train.shape,Y_train.shape)
    print(X_test.shape,Y_test.shape)

# Prints a summary of the model
def printModelSummary(model):
    print(model.summary())

# Evaluates the model
def evaluate(model, X_test, Y_test):
    score, accuracy = model.evaluate(X_test, Y_test, verbose = VERBOSE)
    print("Evaluation:")
    print("  F1 Score: %.2f" % (score))
    print("  Accuracy: %.2f%%\n" % (accuracy * 100))


# Validates the model by extracting a validation set and
# measuring the correct number of guesses
def validate(model, X_test, Y_test):

    X_validate = X_test[-VALIDATION_SIZE:]
    Y_validate = Y_test[-VALIDATION_SIZE:]
    X_test = X_test[:-VALIDATION_SIZE]
    Y_test = Y_test[:-VALIDATION_SIZE]
    score, accuracy = model.evaluate(X_test, Y_test, verbose = VERBOSE,                             batch_size = BATCH_SIZE)
    print("Validation:")
    print("  F1 Score: %.2f" % (score))
    print("  Accuracy: %.2f%%\n" % (accuracy*100))
    print("Getting percentage of correct guesses per political leaning...\n")

    conCount, libCount, conCorrect, libCorrect = 0, 0, 0, 0
    
    for x in range(len(X_validate)):
    
        result = model.predict(X_validate[x].reshape(1, X_test.shape[1]),                                 batch_size = 1, verbose = VERBOSE)[0]
   
        if np.argmax(result) == np.argmax(Y_validate[x]):
            if np.argmax(Y_validate[x]) == 0:
                conCorrect += 1
            else:
                libCorrect += 1
       
        if np.argmax(Y_validate[x]) == 0:
            conCount += 1
        else:
            libCount += 1

    print("Conservative Accuracy:", conCorrect / conCount * 100, "%")
    print("     Liberal Accuracy:", libCorrect / libCount * 100, "%\n")

def save(model):
    model.save(FILE_NAME)               # Creates a HDF5 file to save the whole model
    print("Model saved.\n")             # (e.g. its architecture, weights, and optimizer rate)

#################################### PREPARE DATA ############################################

# Read the data from the CSV file by column
data = pd.read_csv(URL, header = None, names = ['bias', 'text'], sep = SEPERATOR)

# Make all characters lowercase if they are not already
data['text'] = data['text'].apply(lambda x: x.lower())

# Take out all superfluous ASCII characters
data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]', '', x)))

# Eliminate duplicate whitespaces
data['text'] = data['text'].apply((lambda x: re.sub(r'\s+', ' ', x)))

#debug after clean up
# Preprocess texts
tokenizer = Tokenizer(num_words=TOP_WORDS, split=' ')
tokenizer.fit_on_texts(data['text'].values)
X = tokenizer.texts_to_sequences(data['text'].values)
X = pad_sequences(X, maxlen=PADDING_LENGTH)

# Declare the train and test datasets
Y = pd.get_dummies(data['bias']).values
X_train, X_test, Y_train, Y_test =             train_test_split(X, Y, test_size = 0.33, random_state = SEED)

#checkShapes(X_train, X_test, Y_train, Y_test)
# Define the model
model = Sequential()
model.add(Embedding(TOP_WORDS, EMBEDDING_VECTOR_LENGTH, input_length=X.shape[1]))
model.add(LSTM(HIDDEN_LAYER_SIZE))
model.add(Dropout(DROPOUT))
model.add(Dense(2, activation='softmax'))



# %%

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam',                 metrics=['accuracy'])

printModelSummary(model)
print('its working')


# %%

# Stops fitting the model when the improvement is negligible to help prevent over-fitting
earlyStopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=0, verbose=NONVERBOSE, mode='auto')


# %%

# Fit the model
model.fit(X_train, Y_train, validation_data=(X_test, Y_test),             epochs=NUMBER_OF_EPOCHS, batch_size=BATCH_SIZE, callbacks=[earlyStopping])


# %%

print("*" * 75)

# Evaluate the model
evaluate(model, X_test, Y_test)

# Validate the module
validate(model, X_test, Y_test)

print("*" * 75 + '\n')
print('Ended processing here')


# %%

# Save the model
save(model)
print('model saved')


# %%
from keras.models import load_model


# %%
############################### GLOBAL VARIABLES #######################################

# Made these global so both @app.route functions and checkURL can access them.
conservativeURL   = ' '
liberalURL        = ' '
neutralURL        = ' '
cLinkName         = ' '
lLinkName         = ' '
nLinkName         = ' '
errMessage        = ' '
loadedModel       = load_model('finalizedModel.h5')
MAX_REVIEW_LENGTH = 500
TOP_WORDS = 5000                # Most-used words in the article.
NEUTRALBEGIN = 0.4                   # Article is predicted to not be politically biased.
NEUTRALEND = 0.6


# %%

################################### FUNCTIONS ##########################################
from flask import Flask, render_template, request, redirect, url_for
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import Template
import time, requests, numpy
from bs4 import BeautifulSoup
# Runs article through algorithm and determines if it is politically biased and how.
# If politically biased and its biased URL isn't filled, fill its bias' URL slot.
def checkURL(url, text, linkName):
    global conservativeURL
    global liberalURL
    global cLinkName
    global lLinkName
    global neutralURL
    global nLinkName

    # Preprocess article to predict its political bias
    tokenizer = Tokenizer(num_words=TOP_WORDS, split=' ')
    tokenizer.fit_on_texts([text])
    X = tokenizer.texts_to_sequences([text])
    X = pad_sequences(X, maxlen=1000)
    print("Article has been preprocessed and a prediction is being made...")
    
    # Predict if the article is politically biased, and, if so, which way is it biased.
    prediction = loadedModel.predict(X)

    if neutralURL == ' ' and prediction[0][0] <= NEUTRALEND and prediction[0][0] >= NEUTRALBEGIN:
        neutralURL = url
        nLinkName = linkName

    # Fill proper URLs based on prediction.
    elif conservativeURL == ' ' and prediction[0][0] > NEUTRALEND:
            conservativeURL = url
            cLinkName = linkName

    elif liberalURL == ' ' and prediction[0][0] < NEUTRALBEGIN:
            liberalURL = url
            lLinkName = linkName


# %%
testParagraph='Forcing middleclass workers to bear a greater share of the cost of government weakens their support for needed investments and stirs resentment toward those who depend on public services the most '
linkName="Some Article"
print(testParagraph)


# %%
checkURL('CNN.com', testParagraph, linkName)
print(conservativeURL)


# %%
if conservativeURL != ' ' and liberalURL != ' ' and neutralURL != ' ':
    errMessage = "Search for \"" + 'inputString' + "\" has completed"


