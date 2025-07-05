#Joel Atkinson July 5,2025 Assignment 8.2 Database Development & Use

"""import statements"""
import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values

secrets = dotenv_values("../Module-7/.env")

"""database config object"""
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}


#Create function to display films
def show_films(cursor, title):
    cursor.execute('SELECT film_name AS Name, film_director AS Director, genre_name AS Genre,' 
                   'studio_name AS "Studio Name" FROM film INNER JOIN genre ON film.genre_id = genre.genre_id '
                   'INNER JOIN studio ON film.studio_id = studio.studio_id')
    films = cursor.fetchall()

    print('\n-- {} --'.format(title))

    for film in films:
        print('Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n'.format(film[0], film[1],
                                                                                         film[2], film[3]))

try:
    """try/catch block for handling potential MySQL database errors"""

    db = mysql.connector.connect(**config) #connect to movies database

    #output the connection status
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"],
        config["host"], config["database"]))

    input("\n\n Press any key to continue...")

    cursor = db.cursor()

    #Display initial films
    show_films(cursor,'DISPLAYING FILMS')

    #Insert new film
    cursor.execute('INSERT INTO film (film_id, film_name, film_releaseDate, film_runtime, film_director,'
                   'studio_id, genre_id) VALUES(%s, %s, %s, %s, %s, %s, %s)',
                   (4, 'Oppenheimer', 2023, 180, 'Christopher Nolan', 3, 3))

    db.commit()
    show_films(cursor, 'DISPLAYING FILMS AFTER INSERT')#Display films after inserting Oppenheimer

    cursor.execute('UPDATE film SET genre_id = 1 WHERE film_name = "Alien"')#Update Alien to "Horror" genre
    db.commit()
    show_films(cursor, 'DISPLAYING FILMS AFTER UPDATE- changed Alien to Horror')#Display films after updating Alien

    cursor.execute('DELETE FROM film WHERE film_name = "Gladiator"')#Delete Gladiator
    db.commit()
    show_films(cursor, 'DISPLAYING FILMS AFTER DELETE')#Display films after deleting Gladiator


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