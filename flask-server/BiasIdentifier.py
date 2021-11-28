import numpy as np
import pandas
import seaborn as sns
import matplotlib.pyplot as plt


# Keras (2.2.4) and tensorflow (1.13).
import tensorflow as tf
import tensorflow_hub as hub
import tf_sentencepiece

from keras.regularizers import l1, l2
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import backend
from keras import optimizers

#sklearn and imblearn modules:
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from imblearn.over_sampling import SMOTE

p = 0.4
df = pd.read_csv('articles.csv',header=None,skiprows=lambda i: 1>0 and random.random() > p)

#Density:
p = 0.4
df = pd.read_csv('articles2.csv',header=None,skiprows=lambda i: 1>0 and random.random() > p)
#First batch:
n_s_a = df[df[3] == 'Atlantic']
n_s_p = df[df[3] == 'New York Post']
#Second batch:
df = pd.read_csv('articles1.csv',header=None,skiprows=lambda i: 1>0 and random.random() > p)
n_s_b = df[df[3] == 'Breitbart']
n_s_n = df[df[3] == 'New York Times']

n_s = list(n_s_b.iloc[:,9].values) + list(n_s_p.iloc[:,9].values) \
 + list(n_s_a.iloc[:,9].values) + list(n_s_n.iloc[:,9].values)

n_s = [word.replace('New York Post','') for word in n_s]
n_s = [word.replace('Breitbart','') for word in n_s]
n_s = [word.replace('New York Times','') for word in n_s]
n_s = [word.replace('Atlantic','') for word in n_s]

#Outlet classifier:
classes_All = np.asarray([1 for i in range(len(n_s_b))] + \
[2 for i in range(len(n_s_p))] + [3 for i in range(len(n_s_a))] + \
[4 for i in range(len(n_s_n))])
#Bias classifier:
classes_Bias = np.asarray([1 for i in range(len(n_s_b))] + \
[1 for i in range(len(n_s_p))] + [2 for i in range(len(n_s_a))] + \
[2 for i in range(len(n_s_n))])

# Load the encoder:
g = tf.Graph()
with g.as_default():
  text_input = tf.placeholder(dtype=tf.string, shape=[None])
  embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
  embedded_text = embed(text_input)
  init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
g.finalize()

# Initialize session:
session = tf.Session(graph=g)
session.run(init_op)

#Function to compute all embeddings for each sentence:
#Be patient, takes a little while:
def similarity_matrix(merge_list):
    #initialize distance array:
    #initialize embeddings array:
    emb_all = np.zeros([len(merge_list),512])
    #Outer for loop:
    for i in range(0,len(merge_list)):
        #Here is where we run the previously started session, so it is important to run previous step succesfully:
        i_emb = session.run(embedded_text, feed_dict={text_input: [merge_list[i]]})
        emb_all[i,:] = i_emb
    return emb_all

e_All = similarity_matrix(n_s)


#Choose optimizer:
optim = optimizers.Adam(lr=0.00015) 

# create NN for news clissification:
news_DNN = Sequential()
news_DNN.add(Dense(40, input_dim=512, activation = 'relu',kernel_regularizer=l2(0.1)))
news_DNN.add(Dropout(0.25))
news_DNN.add(Dense(40, activation = 'relu',kernel_regularizer=l2(0.1)))
news_DNN.add(Dropout(0.25))


# Output layer with multiclass activation function:
news_DNN.add(Dense(4,activation='softmax'))

# Compile model:
news_DNN.compile(loss='sparse_categorical_crossentropy', optimizer=otim, metrics=['acc'])


# split into shuffled folds:
#Note that you should edit the class array accordingly: Bias (classes_Bias) or Outlet (classes_All)
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.33) # chose one split to make analysis faster. change it if required
for t, te in sss.split(eAll,classes_All):
  # Scale the data with StandardScaler before splitting:
    X_train, X_test = scaler.fit_transform(eAll)[t], \
    scaler.fit_transform(eAll)[te]

    y_train, y_test = classes_All[t]-1,classes_All[te]-1



#fit the network. You can change parameters to see how this affects your training.
m_h = news_DNN.fit(X_train, y_train, epochs=400, \
validation_data=(X_test, y_test), batch_size=32, verbose=0)


from sklearn.metrics import f1_score
f1_score(y_test,news_DNN.predict_classes(X_test))

from sklearn.metrics import f1_score
f1_score(y_test,news_DNN.predict_classes(X_test))
