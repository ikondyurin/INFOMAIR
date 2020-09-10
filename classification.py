##import the data

labels = list()
utterances = list()

with open("dialog_acts.dat", "r") as infile:
  for line in infile:
    label_utterance = line.lower().split(" ", 1)
    labels.append(label_utterance[0])
    utterances.append(label_utterance[1])



#split into train and test
import numpy as np
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(utterances, labels, test_size=0.15)


##vectorize training data
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

#creating bag of words representation
stop_words = set(stopwords.words('english')) 
vectorizer = CountVectorizer(stop_words = stop_words)

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized=vectorizer.transform(X_test)

#classifier logistic regression

def TrainLogisticRegression():
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression(random_state=0).fit(X_train_vectorized, np.reshape(y_train,(-1,1)))
    
    
    y_pred=clf.predict(X_test_vectorized)
    accuracy=clf.score(X_test_vectorized,y_test)
    
    #create confusion matrix
    from sklearn.metrics import confusion_matrix
    cm=confusion_matrix(y_test,y_pred)
    
    from sklearn.metrics import recall_score
    recall=recall_score(y_test, y_pred, average="micro")
    
    from sklearn.metrics import precision_score
    precision=precision_score(y_test, y_pred, average='micro')
    
    from sklearn.metrics import f1_score
    f_score= f1_score(y_test, y_pred, average='micro')
    print("recall, precision and f_score:" ,recall, precision, f_score)
    
    return clf

def TrainNeuralNetwork():
    from sklearn.neural_network import MLPClassifier
    clf = MLPClassifier(random_state=1, max_iter=300)
    clf.fit(X_train_vectorized, np.reshape(y_train,(-1,1)))
            
    y_pred=clf.predict(X_test_vectorized)
    accuracy=clf.score(X_test_vectorized,y_test)
    
    from sklearn.metrics import confusion_matrix
    cm=confusion_matrix(y_test,y_pred)
    
    from sklearn.metrics import recall_score
    recall=recall_score(y_test, y_pred, average="micro")
    
    from sklearn.metrics import precision_score
    precision=precision_score(y_test, y_pred, average='micro')
    
    from sklearn.metrics import f1_score
    f_score= f1_score(y_test, y_pred, average='micro')
    print("recall, precision and f_score:" ,recall, precision, f_score)
    return clf

#user input
while True:
    choice = input("enter 1 for logistic regression, 2 for NN classifier, stop to stop: ")
    if (choice == "1"):
        #classify user utterance
        lr_clf=TrainLogisticRegression()
        while True:
            var=input("enter utterance or enter stop to exit: ")
            if (var != "stop"):
                x=vectorizer.transform([var])
                y=lr_clf.predict(x)
                print("you have entered a "+y[0]+" utterance")
            else:
                break
    elif (choice=="2"):
        nn_clf=TrainNeuralNetwork()
        while True:
            var=input("enter utterance or enter stop to exit: ")
            if (var != "stop"):
                x=vectorizer.transform([var])
                y=nn_clf.predict(x)
                print("you have entered a "+y[0]+" utterance")
            else:
                break
    elif(choice=="stop"):
        break

