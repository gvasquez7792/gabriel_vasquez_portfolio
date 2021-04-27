# create a tool that trains several machine learning models to perform the task of classifying online reviews. Some of these online reviews refer to hazardous products, so these machine learning models will help to identify the most serious product complaints.

import warnings
import time
import json
import requests
import nltk
import sklearn.tree
import sklearn.neighbors
import sklearn.neural_network
import sklearn.model_selection
import sklearn.metrics
import joblib
import math

nltk.download("popular")
warnings.filterwarnings("ignore")
start_time = time.time()  # Timestamp for when process started

response = requests.get(
    "https://dgoldberg.sdsu.edu/515/appliance_reviews.json")


if response:
    data = json.loads(response.text)
    # lists to turn reviews to readable format for sklearn
    reviews = []
    safety = []
    review_safety = []
    unique_words = []
    # sklearn variable lists
    x = []
    y = []

    for line in data:
        # assign each review in lowercase formart
        review = line["Review"].lower()
        # strip all punctuation except apostrophes then append to reviews list
        tokenizer = nltk.RegexpTokenizer(r"[\w']+")
        strip_reviews = tokenizer.tokenize(str(review))
        review = " ".join(strip_reviews)
        reviews.append(review)

        safe = line["Safety hazard"]  # assign each safety hazard value
        safety.append(safe)  # append safe to saftey list
        y.append(safe)  # append safe to sklearn y list
        # create 2D list with safety and reviews
        inner_list = [review, safe]
        review_safety.append(inner_list)

    end_time = time.time()  # Timestamp for when process ended
    time_elasped = end_time - start_time  # Difference between times
    print("\nFinished appending data to lists....", time_elasped, "seconds\n")
    # create unique word lists
    for word in str(reviews).split():
        if word not in unique_words:
            unique_words.append(word)

    end_time = time.time()  # Timestamp for when process ended
    time_elasped = end_time - start_time  # Difference between times
    print("Finished appending unique words.....", time_elasped, "seconds\n")

    # use unique word list to loop through each review/safety and get ABCD variable counts
    A = 0
    B = 0
    variable_A = []
    variable_B = []
    review_countA = []
    review_countB = []
    C = 0
    D = 0
    variable_C = []
    variable_D = []
    for word in unique_words:
        for review, safety in review_safety:
            if safety == 1 and word in review:
                A += 1
            elif safety == 0 and word in review:
                B += 1
            elif safety == 1 and word not in review:
                C += 1
            elif safety == 0 and word not in review:
                D += 1
            review_countA.append(A)
            review_countB.append(B)
            A = 0
            B = 0
        variable_A.append(sum(review_countA))
        variable_B.append(sum(review_countB))
        variable_C.append(C)
        variable_D.append(D)
        review_countA = []
        review_countB = []
        C = 0
        D = 0

    end_time = time.time()  # Timestamp for when process ended
    time_elasped = end_time - start_time  # Difference between times
    print("Finished counting all four variables...", time_elasped, "seconds\n")

    # Calculate unique words relevance scores
    j = 0
    relevant_words = []
    relevance_scores = []
    for word in unique_words:
        try:
            # calculate numerator
            numerator_part1 = math.sqrt(
                variable_A[j] + variable_B[j] + variable_C[j] + variable_D[j])
            numerator_part2 = ((variable_A[j] * variable_D[j]) -
                               (variable_B[j] * variable_C[j]))

            numerator_math = numerator_part1 * numerator_part2
            # calculate denominator
            denominator_math = math.sqrt(
                (variable_A[j] + variable_B[j]) * (variable_C[j] + variable_D[j]))
            # final calculation
            relevance_score = numerator_math / denominator_math
            if relevance_score > 4000:
                relevant_words.append(word)
            relevance_scores.append(relevance_score)
        except:
            relevance_scores.append(0)
        j += 1

    end_time = time.time()  # Timestamp for when process ended
    time_elasped = end_time - start_time  # Difference between times
    print("Finished calculating relevancy scores....\n")

    # create 2D list for taining ML models
    ml_list = []
    for review in reviews:
        col = []
        for word in relevant_words:
            if word in review:
                col.append(1)
            elif word not in review:
                col.append(0)
        ml_list.append(col)

    # create the x and y test & train variables for ML models
    x = ml_list

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        x, y, test_size=0.2, random_state=0)
    # decision tree approach
    dt_clf = sklearn.tree.DecisionTreeClassifier()
    dt_clf = dt_clf.fit(x_train, y_train)
    dt_predictions = dt_clf.predict(x_test)
    dt_accuracy = sklearn.metrics.accuracy_score(y_test, dt_predictions)
    print("Decision tree accuracy: ", dt_accuracy)
    # K nearest neighbor approach
    knn_clf = sklearn.neighbors.KNeighborsClassifier(5)
    knn_clf = knn_clf.fit(x_train, y_train)
    knn_predictions = knn_clf.predict(x_test)
    knn_accuracy = sklearn.metrics.accuracy_score(y_test, knn_predictions)
    print("k-nearest neighbors accuracy: ", knn_accuracy)
    # nerual networks approach
    nn_clf = sklearn.neural_network.MLPClassifier()
    nn_clf = nn_clf.fit(x_train, y_train)
    nn_predictions = nn_clf.predict(x_test)
    nn_accuracy = sklearn.metrics.accuracy_score(y_test, nn_predictions)
    print("Neural network accuracy: ", nn_accuracy, "\n")

    # decide which model is the best approach
    if dt_accuracy > knn_accuracy and dt_accuracy > nn_accuracy:
        print("Decision tree model performed best; saved to hw5model.joblib\n")
        joblib.dump(dt_clf, "hw5model.joblib")
    elif knn_accuracy > dt_accuracy and knn_accuracy > nn_accuracy:
        print("K-nearest neighbor model performed best; saved to hw5model.joblib\n")
        joblib.dump(knn_clf, "hw5model.joblib")
    elif nn_accuracy > dt_accuracy and nn_accuracy > knn_accuracy:
        print("Neural netowrk model performed best; saved to hw5model.joblib\n")
        joblib.dump(nn_clf, "hw5model.joblib")

else:
    print("Error requesting URL, please try again.")
