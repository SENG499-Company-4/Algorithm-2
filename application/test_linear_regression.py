from multiprocessing import connection
import algorithm.linear_regression as linear_regression
from algorithm import py_sqlite as sqlite
import pytest
from math import ceil, floor

# The range in which a prediction can fall 
# (greater or less than) the average capacity for a course 
# Expressed as a percentage
ACCEPTABLE_RANGE = 0.50

pytest.test_model = linear_regression.linear_regression()
db_connection = sqlite.create_connection("./algorithm/database.sqlite")


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


def get_capacities(course, section):
    cur = db_connection.cursor()

    # Get the sum of all capacities of all offerings of this course
    cur.execute('''
                    SELECT SUM(`size`)
                    FROM `courses`
                    WHERE `class_name` LIKE ?
                    AND   `section`    LIKE ?
                    GROUP BY `year`, `semester`
                ''', (course, section))
    all_capacities = cur.fetchall()

    # If there are no values, ignore the 
    if all_capacities == []:
        return linear_regression.linear_regression.defaultCapacity

    max_semester_capacity = all_capacities[0][0]
    min_semester_capacity = all_capacities[0][0]
    for capacity in all_capacities:
        if capacity[0] > max_semester_capacity:
            max_semester_capacity = capacity[0]
        
        if capacity[0] < min_semester_capacity:
            min_semester_capacity = capacity[0]

    capacities = (max_semester_capacity, min_semester_capacity)
    return capacities


def test_capacity_prediction():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT DISTINCT  `class_name`, `semester`
                    FROM `courses`
                    WHERE `size` > 0
                ''')

    course_list = cur.fetchall()
    for course in course_list:
        predicted_capacity = pytest.test_model.predict_size(course[0], course[1])
        capacities = get_capacities(course[0], "A%")

        if predicted_capacity[1] != "Normal":
            continue

        range_max = ceil(capacities[0] * (1 + ACCEPTABLE_RANGE))
        range_min = floor(capacities[1])

        # Assume statements are used instead assert to allow for multiple tests in a single function
        if (not(range_min <= predicted_capacity[0] <= range_max)):
            pytest.assume(range_min <= predicted_capacity[0] <= range_max)