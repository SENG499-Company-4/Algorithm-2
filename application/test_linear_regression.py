from multiprocessing import connection
import algorithm.linear_regression as linear_regression
from algorithm import py_sqlite as sqlite
import pytest

# The range in which a prediction can fall 
# (greater or less than) the average capacity for a course 
# Expressed as a percentage
ACCEPTABLE_RANGE = 0.15

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

def get_average_capacity(course, semester, section):
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT AVG(`size`)
                    FROM `courses`
                    WHERE `class_name` LIKE ?
                    AND   `semester`   LIKE ?
                    AND   `section`    LIKE ?
                ''', (course, semester, section))
    return cur.fetchall()

def test_capcity_preciction():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT DISTINCT `class_name`, `semester`
                    FROM `courses`
                    WHERE `size` > 0
                ''')

    course_list = cur.fetchall()
    for course in course_list:
        predicted_capacity = pytest.test_model.predict_size(course[0], course[1])
        avg_capacity = get_average_capacity(course[0], course[1], "A%")

        if predicted_capacity[1] is not "Normal":
            continue

        range_max = avg_capacity[0][0] * (1 + ACCEPTABLE_RANGE)
        range_min = avg_capacity[0][0] * (1 - ACCEPTABLE_RANGE)
        # Assume statements are used instead assert to allow for multiple tespts in a single function
        pytest.assume(range_min <= predicted_capacity[0] <= range_max)

def main():
    test_linear_model()
    test_db_connection()

if __name__ == "main":
    main()
