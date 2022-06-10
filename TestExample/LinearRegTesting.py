import pandas as pd
from sklearn import linear_model
import json

#Turns JSON file into dict
f = open('sengclasses.json', encoding='utf-8')
classinfo = json.load(f)
classinfo = [x for x in classinfo if x is not None]

#Array to indicate which years data is available for the predicted class
yearfound = [0, 0, 0, 0, 0, 0, 0, 0]

#List of columns made to make future alterations easier
X_columns = ['year1', 'year2', 'year2transfer', 'year3', 'year4', 'year5', 'year6', 'year7']

#2021 Enrolment used to predict 2021 class size
programsize2021 = [113, 90, 15, 93, 74, 44, 10, 2]

if len(X_columns) != len(programsize2021):
    print("Lists 'X_columns' and 'programsize2021' must be of identical length")
    exit()

#Without 2021 enrolment for testing purposes
programsize = {'year': [2020, 2019, 2018, 2017, 2016, 2015, 2014], 
	'year1': [112, 124, 128, 94, 111, 89, 84],
	'year2': [90, 99, 102, 75, 89, 71, 68],
	'year2transfer': [14, 17, 13, 10, 9, 7, 8],
	'year3': [92, 68, 78, 63, 60, 55, 54],
	'year4': [55, 63, 50, 48, 44, 43, 21],
	'year5': [50, 40, 39, 35, 34, 17, 17],
	'year6': [8, 8, 7, 7, 3, 3, 4],
	'year7': [2, 1, 1, 1, 1, 1, 1]}

#List of size for each semester
class_sizes = []

#Stores actual class size in 2021 to compare to prediction
classsize2021 = 0

#Searches through dict to find each class size for specified parameters
for c in classinfo:
    #Looks for correct class, term and section
	if "SENG265" in c['subjectCourse'] and "First Term" in c['termDesc'] and "A02" in c['sequenceNumber']:
        #Determines year class was offered, adds it to class size list and indicates it in yearfound array 
		if "2014" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[6] = 1
		elif "2015" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[5] = 1
		elif "2016" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[4] = 1
		elif "2017" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[3] = 1
		elif "2018" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[2] = 1
		elif "2019" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[1] = 1
		elif "2020" in c['termDesc']:
			class_sizes.insert(0, c['maximumEnrollment'])
			yearfound[0] = 1
		elif "2021" in c['termDesc']:
			classsize2021 = c['maximumEnrollment']

#If class data was not found for a year, remove that year from program enrolment numbers
for x in range(0, 6):
    if yearfound[x] != 1:
        for c in X_columns:
            del programsize[c][x]


#The independant/X values
independent =  pd.DataFrame()
for i in range(0, len(X_columns)):
    independent.insert(i, X_columns[i], programsize[X_columns[i]], True)

#The dependant/Y values
dependent = pd.DataFrame(class_sizes)

#A dataframe containing values that will be used to predict 2021 class capacity
predict_capacities = pd.DataFrame(programsize2021)

#Creates the linear regression model
model = linear_model.LinearRegression()

#Fits the model using independent and dependent values 
model.fit(independent.values, dependent)

print(programsize2021)

print('Predicted 2021 capacity: ', model.predict([programsize2021]))
print('Actual Capacity: ' + str(classsize2021))