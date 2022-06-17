import pandas as pd
from sklearn import linear_model
import json
import csv

years = [2020, 2019, 2018, 2017, 2016, 2015, 2014]


#Hardcoded values for size of each year of enrolment data
program_size = {
    'year1': [112, 124, 128, 94, 111, 89, 84],
    'year2': [90+14, 99+17, 102+13, 75+10, 89+9, 71+7, 68+8],
#   'year2transfer': [14, 17, 13, 10, 9, 7, 8],
    'year3': [92, 68, 78, 63, 60, 55, 54],
    'year4': [55, 63, 50, 48, 44, 43, 21],
    'year5and6': [50+8, 40+8, 39+7, 35+7, 34+3, 17+3, 17+4]
#   'year6': [8, 8, 7, 7, 3, 3, 4],
#   'year7': [2, 1, 1, 1, 1, 1, 1]
    }   

#program_size = {'year1': [112, 124, 128, 94, 111, 89, 84],
#    'year2': [90, 99, 102, 75, 89, 71, 68],
#    'year2transfer': [14, 17, 13, 10, 9, 7, 8],
#    'year3': [92, 68, 78, 63, 60, 55, 54],
#    'year4': [55, 63, 50, 48, 44, 43, 21],
#    'year5': [50, 40, 39, 35, 34, 17, 17],
#    'year6': [8, 8, 7, 7, 3, 3, 4],
#    'year7': [2, 1, 1, 1, 1, 1, 1]}

#Turns JSON file into dict
def CreateDictFromJSON(URL):
    f = open(URL, encoding='utf-8')
    result = json.load(f)
    result = [x for x in result if x is not None]
    return result

def CreatePrediction(class_name, term_name, section):
    class_info = CreateDictFromJSON("sengclasses.json")

    actual_2021_capactity = 0

    #Parameters used to get past class sizes
    #class_name = "SENG499"
    #term_name = "First Term"
    #term_name = "Second Term"
    #term_name = "Summer"
    #section = ""

    #Ensures a class is being searched for
    if class_name == None:
        print("You must enter a class name")
        exit()

    training_data =  pd.DataFrame(dtype='int')

    #Searches through dict to find each class size for specified parameters
    for c in class_info:
        #Looks for correct class plus term and section when they are specified.
        if class_name in c['subjectCourse']:
            if "A" in c['termDesc'] and (term_name in c['termDesc'] or term_name == None): 
                if section in c['sequenceNumber'] or section == None:
                    #Gets int of the year the found class was offered 
                    year_found = int(c["term"][0:4])
                    #Tests if year corresponds to one we have enrolment data for
                    if years[-1] <= year_found <= years[0]:
                        #Creates row of that year's SENG program enrolment data
                        new_row = []
                        for year_sizes in program_size:
                            new_row.append(program_size[year_sizes][years.index(year_found)])
                        #Adds the known course capacity to end of row 
                        new_row.append(int(c['maximumEnrollment']))
                        #Adds row of enrolment data + course capacity to traing data frame
                        training_data = pd.concat([training_data, pd.Series(new_row)], axis=1)
                    #Gets 2021 year to compare result against for testing
                    elif year_found == 2021:
                        actual_2021_capactity = int(c['maximumEnrollment'])

    #Each classes data coresponds to a column when it needs to be in a row
    training_data = training_data.transpose()
    return (training_data, actual_2021_capactity)

open('results.txt', 'w').close()

with open('AllSengClasses.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

f = open("results.txt", "a")

term_names = ["First Term", "Second Term", "Summer"]
sections = ["A01", "A02", "A03", "A04"]
for c in data[0]:
    f.write(c + "\n")
    for t in term_names:
        f.write("   "+t+ "\n")
        for s in sections:
            f.write("       "+s+ "\n")
            training_data, actual_2021_capactity = CreatePrediction(c, t, s)

            #Tests if any results were found and ends program before an error is thrown
            if training_data.empty:
                f.write("           There were no past classes found that match your parameters, retrying with no term"+ "\n")
                training_data, actual_2021_capactity = CreatePrediction(c, "", s)
                if training_data.empty:
                    f.write("           There were no past classes found that match your parameters, retrying with no term and section"+ "\n")
                    training_data, actual_2021_capactity = CreatePrediction(c, "", "")
                    if training_data.empty:
                        f.write("           There were no past classes found that match your parameters"+ "\n")
                        break

            f.write("           There were " + str(len(training_data)) + " enteries for " + c + " " + s + " " + t+ "\n")

            #Creates the linear regression model
            model = linear_model.LinearRegression()

            #Splits training_data data frame into independant and dependant variables for training
            independant_variables = training_data[range(0, len(program_size))]
            dependant_variables = training_data[[len(program_size)]]

            #Fits the model using independent and dependent values 
            model.fit(independant_variables, dependant_variables)

            programsize2021 = [113, 90+15, 93, 74, 44+10]

            #programsize2021 = [113, 90, 15, 93, 74, 44, 10, 2]

            predicted_capacity = int(model.predict([programsize2021])[0][0])
            f.write("           Predicted Capacity " + str(predicted_capacity) + " vs. Actual Capacity " + str(actual_2021_capactity)+ "\n")
        f.write("\n")
    f.write("\n")
