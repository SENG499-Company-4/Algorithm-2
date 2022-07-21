import pandas as pd
from math import ceil
from algorithm import py_sqlite as sqlite
from sklearn import linear_model


class linear_regression:
    years = [2020, 2019, 2018, 2017, 2016, 2015, 2014]  # Used for iterating through database
    semesters = ["Jan", "Sept", "Summer"]
    defaultCapacity = 65  # This is the default size of a class if the algorithm hasn't seen the course before

    def __init__(self):
        # Tests connection to database
        connection = sqlite.create_connection("./application/algorithm/database.sqlite")
        if connection is None:
            print("Failed to connect to database. Exiting.")
            return None

        connection.close()

    def predict_size(self, class_name, semester):
        # Creates a connection to the database
        connection = sqlite.create_connection("./application/algorithm/database.sqlite")
        if connection is None:
            print("Failed to connect to database. Exiting.")
            return None

        if semester.upper() == "FALL":
            semester = self.semesters[1]
        elif semester.upper() == "SPRING":
            semester = self.semesters[0]
        elif semester.upper() == "SUMMER":
            semester.self.semesters[2]

        status = "Normal"

        # Dict where enrolment data is stored before it is turned into dataframe for training
        enrolment_data = {
            'year1': [],
            'year2': [],
            'year3': [],
            'year4': [],
            'year5+': []
        }

        raw_course_data = []

        numberOfMissingYears = 0
        yearsExisting = []
        yearsMissing = []
        for year in self.years:
            # Will return a list if there are multiple sections for a given course. Using "A%" to filter out any
            # tutorial or lab capacities which start with T and B respectively.
            currentCourseData = sqlite.find_course_with_semester(connection, class_name, str(year), "A%", semester)

            # No offering in the given semester for the current year. Record that year as missing
            if len(currentCourseData) == 0:
                yearsMissing.append(year)
                numberOfMissingYears += 1
            else:
                # Found an offering in the given semester.
                raw_course_data.append(currentCourseData)
                yearsExisting.append(year)

        # Loop through and look for capacity values in different semesters for any missing years.
        if 1 < numberOfMissingYears < 8:
            for year in yearsMissing:
                for altSemester in self.semesters:
                    if altSemester == semester:
                        continue
                    currentCourseData = sqlite.find_course_with_semester(connection, class_name, str(year), "A%", altSemester)
                    if len(currentCourseData) != 0:
                        raw_course_data.append(currentCourseData)
                        yearsExisting.append(year)
                        break

        # For years found in alternate semesters, remove the years labelled missing
        for year in yearsExisting:
            if year in yearsMissing:
                numberOfMissingYears -= 1
                yearsMissing.remove(year)

        # If never offered before, new course. Return te default value.
        if numberOfMissingYears == len(self.years):
            connection.close()
            status = "New"
            return ceil(self.defaultCapacity), status

        # Course was offered sporadically in the past. Return average (plus 10%) of the previous capacities.
        predictedCapacity = 0
        if (len(self.years) - numberOfMissingYears) == 2 or (len(self.years) - numberOfMissingYears) == 1:
            for course in raw_course_data:
                if len(course[0]) != 0:
                    predictedCapacity += course[0][0]
            predictedCapacity *= 1.1
            predictedCapacity /= (len(self.years) - numberOfMissingYears)
            connection.close()
            status = "Sporadic"
            return ceil(predictedCapacity), status

        # Sort by year
        raw_course_data.sort(key=lambda x: x[0][2], reverse=True)
        yearsExisting.sort(reverse=True)
        yearsMissing.sort(reverse=True)

        # Iterates through database to get values
        for s in enrolment_data:
            for year in yearsExisting:
                enrolment_data[s].append(sqlite.find_enrollment(connection, str(year), s)[0])

        # This will aggregate all sections of a given course in a given semester and year together creating a
        # total course capacity for that offering of the course.
        course_data = []
        indx = 0
        for course in raw_course_data:
            course_data.append(0)
            for offering in course:
                course_data[indx] += offering[0]
            indx += 1

        # Creates dataframes used for training the model
        independent = pd.DataFrame.from_dict(enrolment_data)
        dependent = pd.DataFrame.from_dict({'course_sizes': course_data})

        # Creates the linear regression model
        model = linear_model.LinearRegression(positive=True)    

        # Fits the model using independent and dependent values
        model.fit(independent.values, dependent)

        # 2021 Values of year size used for testing results
        programsize2021 = [113, 90 + 15, 93, 74, 44 + 10 + 2]

        # The actual predicted 2021 result
        predicted_capacity = int(model.predict([programsize2021])[0][0])

        connection.close()

        # Returns string to be output
        return ceil(predicted_capacity), status
