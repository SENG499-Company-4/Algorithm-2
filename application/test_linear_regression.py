from multiprocessing import connection
import algorithm.linear_regression as linear_regression
from algorithm import py_sqlite as sqlite
import pytest

# The range in which a prediction can fall 
# (greater or less than) the average capacity for a course 
# Expressed as a percentage
ACCEPTABLE_RANGE = 0.2

pytest.test_model = linear_regression.linear_regression()
db_connection = sqlite.create_connection("database.sqlite")

def test_linear_model():
    result = pytest.test_model.predict_size("test")
    assert result.startswith('Predicted'), "linear regression model did not run properly"

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
    result = cur.rowcount()
    assert result > 0, "courses table is not populated"

def test_enrollment_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `enrollment`
                    ''')
    result = cur.rowcount()
    assert result > 0, "enrollment table is not populated"

def test_coefficients_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `coefficients`
                    ''')
    result = cur.rowcount()
    assert result > 0, "coefficients table is not populated"

def get_average_capacity(course):
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT AVG(`size`)
                    FROM `courses`
                    WHERE `class_name` LIKE ?
                ''', (course))
    return cur.fetchall()[0]

def test_capcity_preciction():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT DISTINCT `class_name`
                    FROM `courses`
                    WHERE `size` > 0
                ''')
    course_list = cur.fetchall()
    for course in course_list:
        predicted_capacity = pytest.test_model.predict_size(course)
        avg_capacity = get_average_capacity(course)
        range_max = avg_capacity * (1 + ACCEPTABLE_RANGE)
        range_min = avg_capacity * (1 - ACCEPTABLE_RANGE)
        # Assume statements are used instead assert to allow for multiple tests in a single function
        pytest.assume(predicted_capacity >= range_min and predicted_capacity <= range_max)

def main():
    test_linear_model()
    test_db_connection()

if __name__ == "main":
    main()
