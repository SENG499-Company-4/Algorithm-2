from multiprocessing import connection
from linear_regression import linear_regression
import py_sqlite as sqlite
import pytest

pytest.test_model = linear_regression()
db_connection = sqlite.create_connection("database.sqlite")

def test_linear_model():
    result = pytest.test_model.predict_size("test")
    assert result.startswith('Predicted')

def test_db_connection():
    result = db_connection
    assert result is not None

def test_courses_table_init():
    cur = db_connection.cursor()
    cur.execute(''' 
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='courses' ''')
    result = cur.fetchone()[0] == 1
    assert result is True

def test_enrollment_table_init():
    cur = db_connection.cursor()
    cur.execute(''' 
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='enrollment' ''')
    result = cur.fetchone()[0] == 1
    assert result is True

def test_coefficients_table_init():
    cur = db_connection.cursor()
    cur.execute(''' 
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='coefficients' ''')
    result = cur.fetchone()[0] == 1
    assert result is True

def test_courses_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `courses`
                    ''')
    result = cur.rowcount()
    assert result > 0

def test_enrollment_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `enrollment`
                    ''')
    result = cur.rowcount()
    assert result > 0

def test_coefficients_table_is_populated():
    cur = db_connection.cursor()
    cur.execute('''
                    SELECT *
                    FROM `coefficients`
                    ''')
    result = cur.rowcount()
    assert result > 0

#TODO:
    # figure out a way to test each course in the DB
    # get a list of their past capacities, and make an acceptable range
    # in which the predicted value can fall