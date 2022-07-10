import sqlite3
from sqlite3 import Error
from typing import List

def create_connection(db_file):
    """ 
    Create a database connection to a SQLite database
    If no DB file exists, one will be created
    :param db_file: path to where the db_file will be stored
    :return: 
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        return None
    return conn

def create_table(conn, create_table_sql):
    """ 
    Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_course(conn, course):
    """
    Create a new course into the course table
    :param conn: Connection object
    :param course: list containing the required attributes
    :return: project id
    """
    sql = """ INSERT INTO courses(  class_name
                                ,   year
                                ,   section
                                ,   semester
                                ,   size)
                                    VALUES(?,?,?,?,?) 
                            """
    cur = conn.cursor()
    cur.execute(sql, course)
    conn.commit()
    return cur.lastrowid

def insert_enrollment(conn, enrollment):
    """
    Create a new enrollment tuple into the enrollment table
    :param conn: Connection object
    :param enrollment: list containing the required attributes
    :return: project id
    """
    sql = """ INSERT INTO enrollment(   calendar_year
                                    ,   year_standing
                                    ,   population)
                                        VALUES(?,?,?) 
                                """
    cur = conn.cursor()
    cur.execute(sql, enrollment)
    conn.commit()
    return cur.lastrowid

def insert_coefficient(conn, enrollment):
    """
    Create a new enrollment tuple into the enrollment table
    :param conn: Connection object
    :param enrollment: list containing the required attributes
    :return: project id
    """
    sql = """ INSERT INTO coefficients( class_name
                                    ,   section
                                    ,   semester
                                    ,   year1_coefficient
                                    ,   year2_coefficient
                                    ,   year3_coefficient
                                    ,   year4_coefficient
                                    ,   year56_coefficient)
                                        VALUES(?,?,?) 
                                """
    cur = conn.cursor()
    cur.execute(sql, enrollment)
    conn.commit()
    return cur.lastrowid

def init_tables (conn):
    """
    Create the three required tables for the program
    :param conn: Connection object
    """
    courses = """ 
                CREATE TABLE IF NOT EXISTS courses (
	            course_id INTEGER PRIMARY KEY
	        ,   class_name TEXT NOT NULL
            ,   year TEXT NOT NULL
            ,   section TEXT NOT NULL
            ,   semester TEXT NOT NULL
            ,   size INTEGER DEFAULT -1
                );
            """
    enrollment = """
                CREATE TABLE IF NOT EXISTS enrollment (
                enrollment_id INTEGER PRIMARY KEY
            ,   calendar_year TEXT NOT NULL
            ,   year_standing TEXT NOT NULL
            ,   population INTEGER NOT NULL
                ); 
            """
    coefficients = """
                CREATE TABLE IF NOT EXISTS coefficients (
                coefficient_id INTEGER PRIMARY KEY
            ,   class_name TEXT NOT NULL
            ,   section TEXT NOT NULL
            ,   semester TEXT NOT NULL
            ,   year1_coefficient REAL DEFAULT 0
            ,   year2_coefficient REAL DEFAULT 0
            ,   year3_coefficient REAL DEFAULT 0
            ,   year4_coefficient REAL DEFAULT 0
            ,   year5_coefficient REAL DEFAULT 0
            ,   FOREIGN KEY (class_name, section, semester) 
                    REFERENCES courses (class_name, section, semester)
                );
            """
    
    create_table(conn, courses)
    create_table(conn, enrollment)
    create_table(conn, coefficients)

def find_enrollment(conn, calendar_year: str, year_standing: str) -> int:
    """
    Return a single integer representing the enrollment 
    for that particular calendar year's year standing
    :param conn: Connection object
    :param calender_year: Attribute to search for
    :param year_standing: Attribute to search for
    :return: integer representing that year standing's population in that calendar year
    """
    cur = conn.cursor()
    cur.execute(""" SELECT `population` 
                    FROM `enrollment`
                    WHERE `calendar_year` LIKE ? 
                    AND `year_standing` LIKE ?""",
                    (calendar_year, year_standing))  
    result = cur.fetchall()
    if (result):
        return result[0]
    else:
        return 0

def delete_enrollment(conn, calendar_year: str, year_standing: str):
    """
    Delete any entires matching the two provided parameters
    :param conn: Connection object
    :param calender_year: Attribute to search for
    :param year_standing: Attribute to search for
    """
    cur = conn.cursor()
    cur.execute(""" DELETE FROM `enrollment` 
                    WHERE `calendar_year` LIKE ? 
                    AND `year_standing` LIKE ?""", 
                    (calendar_year, year_standing))
    conn.commit()

def find_course_with_semester(conn, class_name: str, year: str, section: str, semester: str) -> List:
    """
    Finds a course offered in a specific semester
    :param conn: Connection object
    :param class_name: Attribute to search for
    :param year: Attribute to search for
    :param section: Attribute to search for
    :param semester: Attribute to search for
    :return: List of course capacities matching 
    """

    cur = conn.cursor()
    cur.execute(""" SELECT `size`
                    FROM `courses`
                    WHERE `class_name LIKE ?
                    AND `year` LIKE ?
                    AND `section` LIKE ?
                    AND `semester` LIKE ?""",
                    (class_name, year, section, semester))
    return cur.fetchall()

def find_course_no_semester(conn, class_name: str, year: str, section: str) -> List:
    """
    Finds a course offered in any semester
    :param conn: Connection object
    :param class_name: Attribute to search for
    :param year: Attribute to search for
    :param section: Attribute to search for
    :return: List of course capacities matching 
    """

    cur = conn.cursor()
    cur.execute(""" SELECT `size`
                    FROM `courses`
                    WHERE `class_name LIKE ?
                    AND `year` LIKE ?
                    AND `section` LIKE ?""",
                    (class_name, year, section))
    return cur.fetchall()

def delete_course(conn, class_name: str, year: str, section: str, semester: str):
    """
    Deletes a course offering
    :param conn: Connection object
    :param class_name: Attribute to search for
    :param year: Attribute to search for
    :param section: Attribute to search for
    :param semester: Attribute to search for
    """

    cur = conn.cursor()
    cur.execute(""" DELETE FROM `courses`
                    WHERE `class_name` LIKE ?
                    AND `year` LIKE ?
                    AND `section` LIKE ?
                    AND `semester` LIKE ?""",
                    (class_name, year, section, semester))
    conn.commit()

def find_coefficents(conn, class_name: str, section: str, semester: str) -> List:
    """
    Return a list of coefficients related to the desired class
    :param conn: Connection object
    :param class_name: Attribute to search for
    :param year: Attribute to search for
    :param section: Attribute to search for
    :param semester: Attribute to search for
    :return: integer representing that year standing's population in that calendar year
    """

    cur = conn.cursor()
    cur.execute(""" SELECT  `year1_coefficient`
                        ,   `year2_coefficient` 
                        ,   `year3_coefficient` 
                        ,   `year4_coefficient` 
                        ,   `year5_coefficient`
                    FROM `coefficients`
                    WHERE `class_name` LIKE ?
                    AND `section` LIKE ?
                    AND `semester` LIKE ?""",
                    (class_name, section, semester))
    return cur.fetchall()

def delete_coefficients(conn, class_name: str, section: str, semester: str):
    """
    Delete the tuple of coefficients related to the desired class
    :param conn: Connection object
    :param class_name: Attribute to search for
    :param year: Attribute to search for
    :param section: Attribute to search for
    :param semester: Attribute to search for
    """

    cur = conn.cursor()
    cur.execute(""" DELETE FROM `coefficients`
                    WHERE `class_name` LIKE ?
                    AND `section` LIKE ?
                    AND `semester` LIKE ?""",
                    (class_name, section, semester))
    conn.commit()

if __name__ == "__main__":
    conn = create_connection("./algo2_sqlite.db")
    init_tables(conn)
    #insert_enrollment(conn, ("2020", "3", 500))
    print("Returned value: " + str(find_enrollment(conn, "2020", "3")))
    delete_enrollment(conn, "2020", "3")
