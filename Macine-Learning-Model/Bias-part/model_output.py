# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from flask import Flask, render_template, request, redirect, url_for
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import Template
import time, requests, numpy
from bs4 import BeautifulSoup


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
    print("Prediction: ", prediction)
    print('Result: ', prediction[0])
    print('Result:', prediction[0][0])
    print('Result:', prediction[0][1])
    if neutralURL == ' ' and prediction[0][0] <= NEUTRALEND and prediction[0][0] >= NEUTRALBEGIN:
        print('neutral')
        neutralURL = url
        nLinkName = linkName

    # Fill proper URLs based on prediction.
    elif conservativeURL == ' ' and prediction[0][0] > NEUTRALEND:
            print('Conservative')
            conservativeURL = url
            cLinkName = linkName

    elif liberalURL == ' ' and prediction[0][0] < NEUTRALBEGIN:
            print('Liberal')
            liberalURL = url
            lLinkName = linkName
    print('Variables')
    print(neutralURL, nLinkName, conservativeURL, cLinkName, liberalURL, lLinkName)

print('its working')


# %%
def results():
    global conservativeURL
    global liberalURL
    global neutralURL
    global cLinkName
    global lLinkName
    global nLinkName
    global errMessage
    global tokenizer

    # Need to clear these fields to run another query
    conservativeURL = ' '
    liberalURL      = ' '
    neutralURL      = ' '
    cLinkName       = ' '
    lLinkName       = ' '
    nLinkName       = ' '
    errMessage      = ' '
    
    
    inputString = 'coronavirus vaccine'
    # driver = webdriver.PhantomJS()    # Creates an invisible browser.
    # driver.get('https://google.com/') # Navigates to Google.com.
    # searchBarInput = driver.find_element_by_name('q') # Assigns query to Google Search bar.
    if inputString != '':
        print('You Searched for: ',inputString)

    linkName="CNN Article"
    paragraphs='''President Trump's executive order curtailing immigration "could do long-term damage" to the United States' national security and foreign policy interests, endangering troops and intelligence agents and disrupting efforts to prevent terror attacks, 10 former senior U.S. diplomats and security officials asserted Monday in a court document. The affidavit,
     written jointly by two former secretaries of state, two former heads of the CIA, a former secretary of defense, a former secretary of homeland security, and senior officials of the National Security Council, slammed Trump’s order as “ill-conceived, poorly implemented and ill-explained.'''
    url="CNN.com"
    checkURL(url, paragraphs, linkName)
    # print('conservative url', conservativeURL)
    
    print('its working')
        
results()
if conservativeURL !='' and liberalURL != '':
        errMessage="Search for" + 'inputString'+ "has been completed"
        


