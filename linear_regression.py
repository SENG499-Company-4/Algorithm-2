import py_sqlite as sqlite
import pandas as pd
from sklearn import linear_model

class linear_regression:
	years = [2020, 2019, 2018, 2017, 2016, 2015, 2014]	#Used for iterating through database

	def __init__(self):
		#Used to add values to the database if they don't already exist
		programsize = {	'year1': [112, 124, 128, 94, 111, 89, 84],
		'year2': [90+14, 99+17, 102+13, 75+10, 89+9, 71+7, 68+8],
		#'year2transfer': [14, 17, 13, 10, 9, 7, 8],
		'year3': [92, 68, 78, 63, 60, 55, 54],
		'year4': [55, 63, 50, 48, 44, 43, 21],
		'year5+': [50+8, 40+8, 39+7, 35+7, 34+3, 17+3, 17+4],
		#'year6': [8, 8, 7, 7, 3, 3, 4]
		}

		#Creates connection to database
		connection = sqlite.create_connection("database.sqlite")
		if connection is None:
			print("Failed to connect to database. Exiting.")
			return None
		sqlite.init_tables(connection)

		#Iterates through program data and adds enrolment data if it does not exist
		for s in programsize:
			for y in self.years:
				if not sqlite.find_enrollment(connection, str(y), s):
					sqlite.insert_enrollment(connection, (str(y), s, programsize[s][(self.years[0])-y]))

		connection.close()

	def predict_size(self, class_name):
		#Creates a connection to the database
		connection = sqlite.create_connection("database.sqlite")
		if connection is None:
			print("Failed to connect to database. Exiting.")
			return None

		#Dict where enrolment data is stored before it is turned into dataframe for training
		enrolment_data = {
			'year1': [],
			'year2': [],
			'year3': [],
			'year4': [],
			'year5+': []
			}

		#Iterates through database to get values
		for s in enrolment_data:
			for year in self.years:
				enrolment_data[s].append(sqlite.find_enrollment(connection, year, s)[0])
		
		#Hard coded exaple data for SENG360 A02 Sept-Dec term
		seng_310_example_data= [60, 56, 52, 62, 52, 40, 35]

		#Creates dataframes used for training the model
		independent =  pd.DataFrame.from_dict(enrolment_data)
		dependent = pd.DataFrame.from_dict({'course_sizes': seng_310_example_data})

		#Creates the linear regression model
		model = linear_model.LinearRegression()

		#Fits the model using independent and dependent values 
		model.fit(independent.values, dependent)

		#2021 Values used for testing results
		programsize2021 = [113, 90+15, 93, 74, 44+10]
		expected_2021_data = 82

		#The actual predicted 2021 result
		predicted_capacity = int(model.predict([programsize2021])[0][0])

		connection.close()

		#Returns string to be output
		return("Predicted 2021 Capacity for SENG310 Fall A02 " + str(predicted_capacity) + " vs. Actual Capacity for SENG310 Fall A02 " + str(expected_2021_data))