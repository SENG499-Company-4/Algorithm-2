import py_sqlite as sqlite
import json
class create_db:
	years = [2020, 2019, 2018, 2017, 2016, 2015, 2014]	#Used for iterating through database

	def __init__(self):
		print("Could not find database. Creating new one.")
		#Used to add values to the database if they don't already exist
		programsize = {	'year1': [113, 112, 124, 128, 94, 111, 89, 84],
		'year2': [90+15, 90+14, 99+17, 102+13, 75+10, 89+9, 71+7, 68+8],
		'year3': [93, 92, 68, 78, 63, 60, 55, 54],
		'year4': [74, 55, 63, 50, 48, 44, 43, 21],
		'year5+': [44+10, 50+8, 40+8, 39+7, 35+7, 34+3, 17+3, 17+4],
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

		# Opening JSON file
		f = open('course_data.json')
		course_data = json.load(f)

		for course in course_data:
			sqlite.insert_course(connection, [course['subject']+course['course'], course['year'], course['section'], course['semester'], course['size']])

		connection.close()