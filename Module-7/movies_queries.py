#Joel Atkinson July 3,2025 Assignment 7.2 Database Dev & Use CSD-310

"""import statements"""
import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values

secrets = dotenv_values(".env")

"""database config object"""
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """try/catch block for handling potential MySQL database errors"""

    db = mysql.connector.connect(**config) #connect to movies database

    #output the connection status
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"],
        config["host"], config["database"]))



    input("\n\n Press any key to continue...")

    # Add Cursor for queries
    cursor = db.cursor()

    # First Query
    print('\n -- DISPLAYING Studio RECORDS --')
    cursor.execute('SELECT * FROM studio')
    studios = cursor.fetchall()
    for studio in studios:
        print(f'Studio ID: {studio[0]}')
        print(f'Studio Name: {studio[1]}')
        print()

    # Second Query
    print('\n-- DISPLAYING Genre RECORDS --')
    cursor.execute('SELECT * FROM genre')
    genres = cursor.fetchall()
    for genre in genres:
        print(f'Genre ID: {genre[0]}')
        print(f'Genre Name: {genre[1]}')
        print()

    # Third Query
    print('\n-- DISPLAYING Short Film RECORDS --')
    cursor.execute('SELECT film_name, film_runtime FROM film WHERE film_runtime < 120')
    short_films = cursor.fetchall()
    for film in short_films:
        print(f'Film Name: {film[0]}')
        print(f'Runtime: {film[1]}')
        print()

    # Fourth Query
    print('\n-- DISPLAYING Director RECORDS in Order --')
    cursor.execute('SELECT film_director, film_name FROM film ORDER BY film_director')
    film_data = cursor.fetchall()
    for film in film_data:
        if film[0] and film[1]:
            print(f'Film Name: {film[1]}')
            print(f'Film Director: {film[0]}')
            print()


except mysql.connector.Error as err:
    """on error code"""

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)

finally:
    """close the connection to MySQL"""
    cursor.close()
    db.close()