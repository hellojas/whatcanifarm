########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	this file was used to experiment with many different
#	machine learning algorithms. it was mostly used in
#	an ipython notebook so it is not organized 
#	as object oriented classes and methods. 
#######################################################

import numpy as np
import ast
import pandas as pd
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
import pydot 
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.externals.six import StringIO  
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import label_ranking_average_precision_score
from sklearn.metrics import coverage_error
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import hamming_loss
from sklearn.metrics import average_precision_score
import re
from sklearn.externals import joblib
from sklearn.svm import SVC 
import pickle

'''
dataset class that facilitates the input for
sklearn classifiers;

the classifier will use:
X = the values
y = the target label_ranking_average_precision_score
X_imp = the values after a mean imputer
y_bin = target values after MultiLabelBinarizer

@param filename, is filename with features (X)
@param cropsfile, is target labels
@param name, is name of this dataset
'''
class dataset():
    def __init__(self,filename,cropsfile,name):
#         self.dir = dir
        self.filename = filename
        self.cropsfile = cropsfile
        self.dataset = []
        self.featureNames = []
        self.name = ""
        self.X = []
        self.X_imp = []
        self.y = []
        self.y_bin = []
        self.n_samples = 0
        self.n_features = 0


    '''
    read the dataset
    run this method after init dataset()
    to read the files into the variables
    '''
    def read(self):
        dataset = pd.read_csv(self.filename, header =0, index_col=0)
        crops = pd.read_table(self.cropsfile, header=None, index_col=None)
        self.X = dataset
        y_temp = crops
        self.featureNames = self.X.columns
        self.n_samples = self.X.shape[0]
        self.n_features = self.X.shape[1]
        for y_i in crops.values:
            y_i = str(y_i).replace("[","").replace("]","").replace("\"","")
            newlist = []
            for x in str(y_i).split(","):
                if len(re.sub(r'\W+', ' ', x.replace("\'","")).strip()) != 0:
                    newlist.append(re.sub(r'\W+', ' ', x.replace("\'","")).strip())
            self.y.append(newlist)

    '''
    run an imputer on missing values for X values
    run this method after self.read()
    sets X_imp value automatically

    @param imp_type can be 'mean', 'mode' 
    @see sklearn docs for detailed exp
    '''        
    def imputer(self,imp_type):
        imp = Imputer(missing_values='NaN', strategy=imp_type)
        self.X_imp = imp.fit_transform(self.X, self.y)

'''
generates a decision tree classifier 
based on a given dataset

@see sklearn docs for detailed exp
@param dataset, dataset() class after read()
@return clf, the classifier generated
'''   
def decisionTree(dataset):
    print ("generating decision tree...")
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(dataset.X_imp,dataset.y)
    return clf
 
'''
exports a PDF for the decision tree to
visualize the splitting and feature hiearchy

@param clf, the decision tree classifier 
@param dataset, dataset() class after read()
@param fileout, the file to save to
@outputfile, pdf file
'''     
def toPdf(clf,dataset,fileout):
    dot_data = StringIO() 
    tree.export_graphviz(clf, out_file=dot_data, feature_names=dataset.featureNames) 
    graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
    graph.write_pdf("RF_all_multilabel_2014/"+fileout+".pdf") 

'''
pretty print the top ten in a list
assumes it is sorted descending

@param L, sorted list descending
'''     
def printTopTen(L):
    for i,l in enumerate(L):
        print l
        if i == 10:
            break

'''
loops through a one vs all classifier for
all classifiers and generates a pdf for each
tree

@param OVR_Clf, the one v all classifier
@param mlb, the MultiLabelBinarizer used
@param modelData, a dataset() object
'''     
def genAllPdfs(OVR_Clf, mlb, modelData):
    print ("writing to pdf...")
    for i,dt in enumerate(OVR_Clf.estimators_[50:100]): 
        if type(dt) is DecisionTreeClassifier:
            toPdf(dt, modelData,mlb.classes_[i][0:80])
 
'''
* NOTE this object is used in the web app *

the model object that saves everything needed to
faciliate the web application 

required:
input = values to predict on for each zipvode,
i.e. new weather conditions (not trained on)
classifier = the one v all classifier
validZips = restricting what zipcodes the user can enter
farms = list of organic farms by zipcode
mlb = MultiLabelBinarizer used for the classifier
'''   
 class model():
    def __init__(self, input, classifier, mlb, validZips, us_farms ):
        self.input = input
        self.classifier = classifier
        self.validZips = validZips
        self.farms = us_farms
        self.mlb = mlb

    '''
    gets a list of organic farms by zipcode
    @param zip, the zipcode to query
    @return the list of farms for that zipcode
    '''  
    def getFarms(self, zip):
         return self.farms[self.farms["Zip_Code"] == int(zip)]

    '''
    validates the zipcode query in validZips 
    and return the feature vector
    @param zip, the zipcode to query
    @return the feature vector for the zipcode
    if is valid or None
    '''  
    def submitZip(self, zip):
        if int(zip) in self.validZips:
            return self.input[self.input.index==int(zip)]
        else:
            return None

    '''
    use the classifier to predict the probabilities
    based on the input returned from submitZip
    @param x_input, from submitZip
    @param limit, limit the returned list to top #
    @return top # of rankings
    '''  
    def predict(self,x_input,limit):
        prediction = np.zeros(x_input.shape[1])
        x = x_input
        probabilities = np.zeros(self.mlb.classes_.shape)
        for c in range(len(self.classifier.estimators_)):
            probabilities[c] = self.classifier.estimators_[c].predict_proba(x)[0][1]
#         prediction[i] = np.argmax( probabilities )
        rankings = zip(self.mlb.classes_, probabilities)
        rankings.sort(key=lambda x: x[1],reverse=True)
        return rankings[0:limit]
#         printTopTen(zipped)
               

if __name__ == "__main__":

	weatherImpMean = pd.read_csv("weather2015.csv")
	zips = pd.read_csv("us_zips.csv")
	us_farms = pd.read_csv("us_farms.csv")

	''' decision tree'''

	# LOADING DATASET
	rng = np.random.RandomState(0)
	filename = "features_list_unique_2014.csv"
	crops = "crops_list_unique_2014.txt"
	modelData = dataset(filename,crops,"farms_dt")
	modelData.read()

	# PROCESS
	modelData.imputer("mean")
	model = decisionTree(modelData)
	toPdf(model, modelData)
	print "done"

	''' one vs all classifiers '''

	# LOADING DATASET
	mlb = MultiLabelBinarizer()
	modelData.y_bin = mlb.fit_transform(modelData.y)
	X_train, X_test, y_train, y_test = train_test_split(modelData.X_imp, modelData.y_bin, test_size=0.2, random_state=0)
	OVR_Clf = OneVsRestClassifier(DecisionTreeClassifier(criterion="gini",splitter="best",max_features=modelData.n_features/10)).fit(X_train, y_train)
	OVR_Clf_RF = OneVsRestClassifier(RandomForestClassifier(class_weight='auto', n_estimators = 15,min_samples_split =25)).fit(X_train, y_train)

	# CREATE GREEN FARMS MODEL for app
	greenfarms = model(weatherImpMean, OVR_Clf_RF, mlb, zips, us_farms)

	# test one zip
	z = 10013
	x = greenfarms.submitZip(z)
	if x is not None:
	    pred = pd.DataFrame(greenfarms.predict(x), columns=["Class","Prob"])
	    farms = greenfarms.getFarms(z)
	print farms
	print pred

    ## dump for model using pickle
	# joblib.dump(weatherImpMean, 'input.pkl', compress=9)
	# joblib.dump(OVR_Clf_RF, 'classifier.pkl', compress=9)
	# joblib.dump(mlb, 'mlb.pkl', compress=9)
	# joblib.dump(us_farms, 'farms.pkl', compress=9)
	# joblib.dump(zips, 'us_zips.pkl', compress=9)


