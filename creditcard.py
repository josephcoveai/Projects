import csv
import numpy as np
import random


'''
This code can take a few minutes to run
It will print the header of the credit card file
Then it will print the results on test data in real time
Then it will print the aggregate of those results

If I were to write an algorithm like this for a bank to use,
I would probably cluster the training data and calculate centroids to
measure the distance against in the testing data to increase 
the computational efficiency of testing at the expense of more time training

The randomly generated testing data should be about half fraud and half legitimate
While the data set contains only 0.17% fraud

The dataset code not fit into github but can be downloaded at https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

'''


def minkowski_distance(x, y, p):
    '''
    Calculate the Minkowski distance between the first 30 features of 2 vectors
    
    Parameters:
    x(list): first vector
    y(list): second vector
    p(int): order of the norm
    
    Returns:
    distance between them (float)
    '''
    distance = 0
    for i in range(30):
        distance += abs(x[i] - y[i]) ** p
    
    distance = distance ** (1/p)
    return distance


def make_corr_list(training):
    '''
    Identify the correlation between each variable and the value
    
    Parameters:
    training (list of lists): training data
    
    Returns:
    corr_list: a list of correlation between each feature and the label by index
    '''
    corr_list = []
    cc_array = np.array(training)
    corr_array = np.flip(np.transpose(cc_array))
    n_rows = corr_array.shape[0]
    for i in range(n_rows):
        corr_coef = np.corrcoef(corr_array[i, :], corr_array[-1, :])[0, 1]
        corr_list.append(corr_coef)
    for i in range(len(corr_list)):
        corr_list[i] *= 100
    return corr_list


def scale_feature_vectors(corr_list, feature_vectors):
    '''
    Scales the feature vectors to amplify features based on their correlation to
    the label.
    
    Parameters:
    corr_list (list): correlation of each feature to the outcome
    feature_vectors (list of lists): list of feature vectors to alter
    
    Returns:
    Null
    '''
    for a in range(len(feature_vectors)):
        for b in range(30):
            feature_vectors[a][b] *= corr_list[b]
        
def knn(k, p, training, v):
    """
    Finds the k closest lists in the training set to the input v,
    using the Minkowski distance with exponent p.
    
    Parameters:
    k (int): the number of closest lists to find
    p (float): the exponent of the Minkowski distance function
    training (list of lists): the training set of lists
    v (list): the input list
    
    Returns:
    list: a list of length k containing the k closest lists in the training set to v
    """
    
    distances = [minkowski_distance(x, v, p) for x in training]
    indices = sorted(range(len(distances)), key=lambda i: distances[i])[:k]
    return indices

def flag(training, indices):
    """
    Determines whether a transaction is potentially fraudulent based on
    the feature vectors proximity to known feature vectors
    
    Parameters:
    training (list of lists): the training set of lists
    indices (list): indices of the closest lists
    
    Returns:
    either string safe or flag depeding on if a close neighbor in the
    training data is fraudulent
    """
    for i in indices:
        if training[i][30] == 1.0:
            return "flag"
    return "safe"

def results(training, testing):
    '''
    Calculates the effectiveness of the algorithm on testing data
    
    Parameters:
    training (list of lists): the training set of lists
    testing (list of lists): the testing set of lists
    
    Returns:
    Null, it prints the results
    
    '''
    fraud = 0
    leg = 0
    detected = 0
    f_positive = 0
    for i in range(len(testing)):
        indices = knn(4, 1, training, testing[i])
        r = flag(training, indices)
        if r == "flag":
            if testing[i][30] == 1.0:
                detected += 1
                fraud += 1
                print("Detected Fraud")
            else:
                leg += 1
                f_positive += 1
                print("False Positive")
        else:
            if testing[i][30] == 1.0:
                fraud += 1
                print("Undetected Fraud")
            else:
                leg += 1
                print("Legitimate Transaction")
    print("")
    print(f"This algorithm flagged {round(detected*100/fraud, 2)}% of fraudulent transactions in the testing data")
    print(f"This algorithm flagged {round(f_positive*100/leg, 2)}% of legitimate transactions in the testing data")    

def main():
    # Read credit card data into cc_data
    with open('creditcard.csv', 'r') as f:
        reader = csv.reader(f)
        cc_data = []
        for row in reader:
            cc_data.append(row)
    # Print header of credit card data
    print(cc_data[0])
    print("")
    # 0 is time, 28 PCA varoiables, 29 is Amount, 30 is label
    # Format the data
    # Remove header
    cc_data = cc_data[1:]
    # Convert to floats
    for a in range(len(cc_data)):
        for b in range(len(cc_data[a])):
            cc_data[a][b] = float(cc_data[a][b])
    # Seperate data into training and testing
    training = []
    testing = []
    for row in cc_data:
        if row[30] == 1.0 and random.random() < .02:
            testing.append(row)
        elif row[30] == 0.0 and random.random() < .000035:
            testing.append(row)
        else:
            training.append(row)
    # Correlation
    corr_list = make_corr_list(training)
    corr_list = corr_list[:-1]
    # Scale the feature vectors
    scale_feature_vectors(corr_list, training)
    scale_feature_vectors(corr_list, testing)
    # Calculate distance
    results(training, testing)

    
    
if __name__=="__main__":
    main()
