from multiprocessing import connection
import algorithm.linear_regression as linear_regression
from algorithm import py_sqlite as sqlite
import pytest
from math import ceil

# The range in which a prediction can fall 
# (greater or less than) the average capacity for a course 
# Expressed as a percentage
ACCEPTABLE_RANGE = 0.25

pytest.test_model = linear_regression.linear_regression()
db_connection = sqlite.create_connection("./application/algorithm/database.sqlite")

def test_db_connection():
    result = db_connection
    assert result is not None, "connection to SQLite DB does not exist"

def test_courses_table_init():
    cur = db_connection.cursor()
    cur.execute(''' 
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='courses' ''')
    result = cur.fetchone()[0] == 1
    assert result is True, "courses table does not exist"

def test_enrollment_table_init():
    cur = db_connection.cursor()
    cur.execute(''' 
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='enrollment' ''')
    result = cur.fetchone()[0] == 1
    assert result is True, "enrollment table does not exist"

def test_coefficients_table_init():
    cur = db_connection.cursor()
    cur.execute(''' 
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='coefficients' ''')
    result = cur.fetchone()[0] == 1
    assert result is True, "coefficients table does not exist"

def test_courses_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `courses`
                    ''')
    result = cur.arraysize
    assert result > 0, "courses table is not populated"

def test_enrollment_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `enrollment`
                    ''')
    result = cur.arraysize
    assert result > 0, "enrollment table is not populated"

def test_coefficients_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `coefficients`
                    ''')
    result = cur.arraysize
    assert result > 0, "coefficients table is not populated"

def get_average_capacity(course, semester, section):
    cur = db_connection.cursor()

    #
    # Start of debugging stuff
    cur.execute('''
                    SELECT SUM(`size`), `semester`, COUNT(*)
                    FROM `courses`
                    WHERE `class_name` LIKE "SENG310"
                    AND `section` LIKE "A%"
                    AND `semester` LIKE ?           
                ''', (semester,))
    #print(cur.fetchall())

    # End of debugging stuff
    #

    # Get the sum of all capacities of all offerings of this course
    cur.execute('''
                    SELECT SUM(`size`)
                    FROM `courses`
                    WHERE `class_name` LIKE ?
                    AND   `semester`   LIKE ?
                    AND   `section`    LIKE ?
                ''', (course, semester, section))
    total_capacity = cur.fetchall()
    if total_capacity[0][0] is None:
        return linear_regression.linear_regression.defaultCapacity

    # Get the number of distinct semesters in which this course was offered
    cur.execute('''
                    SELECT COUNT (*)
                    FROM    (
                            SELECT DISTINCT `year`, `semester`
                            FROM `courses`
                            WHERE `class_name` LIKE ?
                            AND   `semester`   LIKE ?
                            AND   `section`    LIKE ?  
                            )  
                ''', (course, semester, section))
    num_offerings = cur.fetchall()
    return ceil((total_capacity[0][0] / num_offerings[0][0]))

def test_capcity_preciction():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT DISTINCT  `class_name`, `semester`
                    FROM `courses`
                    WHERE `size` > 0
                ''')

    course_list = cur.fetchall()
    for course in course_list:
        predicted_capacity = pytest.test_model.predict_size(course[0], course[1])
        avg_capacity = get_average_capacity(course[0], course[1], "A%")

        if predicted_capacity[1] != "Normal":
            continue

        range_max = ceil(avg_capacity * (1 + ACCEPTABLE_RANGE))
        range_min = ceil(avg_capacity * (1 - ACCEPTABLE_RANGE))

        # if (str(course[0]) == "SENG310"):
        #     print("Course: " + course[0] + ", semester: " + course[1] + ", range_max: " + str(range_max) + ", range_min: " + str(range_min) + ", pred_value: " + str(predicted_capacity[0]))
        # else:
        #     continue
        
        # Assume statements are used instead assert to allow for multiple tests in a single function
        if (not(range_min <= predicted_capacity[0] <= range_max)):
            pytest.assume(range_min <= predicted_capacity[0] <= range_max)