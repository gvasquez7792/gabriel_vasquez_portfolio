# Description: This program detects if an email is spam (1) or not (0)
# Sources: https://randerson112358.medium.com/email-spam-detection-using-python-machine-learning-abe38c889855

# Import Libraries
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
import numpy as np
import pandas as pd
import string
nltk.download("popular")
# Read the CSV file containing emails to test
data_frame = pd.read_csv('email_spam_or_not_spam.csv')

# print the first 5 rows of data
data_frame.head(5)

# Print the shape (Get the number of rows and columns)
data_frame.shape

# Get the columns names
data_frame.columns

# Check for duplicates and remove them
data_frame.drop_duplicates(inplace=True)

# show the new shape (number of rows and columns)
data_frame.shape

# show the number of missing (NAN, Nan, na) data for each column
data_frame.isnull().sum()


def process_text(text):
    # 1 remove the punctuation
    # 2 remove stopwords
    # 3 return a list of clean text words

    # 1
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)

    # 2
    clean_words = [word for word in nopunc.split() if word.lower()
                   not in stopwords.words('english')]

    # 3
    return clean_words


# Show the tokenization (a list of tokens also called lemmas)
data_frame['text'].head().apply(process_text)

# Example
message1 = 'hello world hello hello world play'
message2 = 'test test test one hello'
print(message1)
print()

# Convert the text to a matrix of token counts
bow4 = CountVectorizer(analyzer=process_text).fit_transform(
    [[message1], [message2]])
print(bow4)
print()
print(bow4.shape)

# Convert a collection of text to a matrix of tokens ('bag of words')
messages_bow = CountVectorizer(
    analyzer=process_text).fit_transform(data_frame['text'])

# Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(
    messages_bow, data_frame['spam'], test_size=0.2, random_state=0)

# Get the shape of messages_bow
messages_bow.shape

# Create and train the Naive Bayes Classifier
classifier = MultinomialNB().fit(x_train, y_train)

# print the predictions
print(classifier.predict(x_train))

# print the actual values
print(y_train.values)

# Evaluate the model on the training data set
pred = classifier.predict(x_train)
print(classification_report(y_train, pred))
print()
print('Confusion Matrix: \n', confusion_matrix(y_train, pred))
print()
print("Accuracy: ", accuracy_score(y_train, pred))

# print the test predictions
print(classifier.predict(x_test))

# print the test actual values
print(y_test.values)

# Evaluate the model on the test data set
pred = classifier.predict(x_test)
print(classification_report(y_test, pred))
print()
print('Confusion Matrix: \n', confusion_matrix(y_test, pred))
print()
print("Accuracy: ", accuracy_score(y_test, pred))
