from bottle import route, post, run, response, request
from urllib.parse import unquote
import sqlite3
import json

db = sqlite3.connect("movies.sqlite")

@route('/hello')
def hello():
    return "Hello World!"

### /ping
## GET
# should return pong and status 200
@route('/ping')
def ping():
    response.status = 200
    return "pong"

@route('/bing_bong')
def bing_bong():
    return "fuck ya life, BING BONG!"

### /reset
## POST
# empties the database, and enters the following theaters:
#
#    “Kino”, 10 seats
#    “Regal”, 16 seats
#    “Skandia”, 100 seats
@route('/reset')
def reset():
    c = db.cursor()

    tables = ["theaters", "screenings", "customers", "movies", "tickets"]
    for t in tables:
        c.execute(f"DROP TABLE IF EXISTS {t}")

    c.execute("""
        CREATE TABLE theaters (
            name     TEXT,
            capacity INT,
            PRIMARY KEY(name)
        );"""
    )

    c.execute("""
        CREATE TABLE screenings (
            screening_id    TEXT DEFAULT(lower(hex(randomblob(16)))),
            start_time      TIME,
            start_date      DATE,
            t_name          TEXT,
            imdb_key        TEXT,
            PRIMARY KEY(screening_id),
            FOREIGN KEY(imdb_key) REFERENCES movies(imdb_key),
            FOREIGN KEY(t_name) REFERENCES theaters(name)
        );"""
    )
    c.execute("""
        CREATE TABLE customers (
            username    TEXT,
            password    TEXT,
            first_name  TEXT,
            last_name   TEXT,
            PRIMARY KEY(username)
        );"""
    )

    c.execute("""
        CREATE TABLE movies (
            year            INT,
            title           TEXT,
            imdb_key        TEXT,
            PRIMARY KEY(imdb_key)
        );"""
    )
    # running_time    INT,

    c.execute("""
        CREATE TABLE tickets (
            ticket_id       TEXT DEFAULT(lower(hex(randomblob(16)))),
            username        TEXT,
            screening_id    TEXT,
            PRIMARY KEY(ticket_id),
            FOREIGN KEY(username) REFERENCES customers(username),
            FOREIGN KEY(screening_id) REFERENCES screenings(screening_id)
        );"""
    )

    c.execute(
        """
        INSERT
        INTO theaters(name, capacity)
        VALUES ("Kino", 10),
               ("Regal", 16),
               ("Skandia", 100);
        """
    )
    return

### /users
##  POST
# Create a new user with a JSON-request such as this one:
#
# {
#     "username": "alice",
#     "fullName": "Alice Lidell",
#     "pwd": "aliceswaytoosimplepassword"
# }
#
# If the username is taken, return 400, otherwise return /users/<username> in a 201
# curl -X POST http://localhost:7007/users -H "Content-Type: application/json" --data "@names.json"
@post("/users")
def users():
    credentials = request.json
    c = db.cursor()
    # TODO: (optional) encrypted password
    try:
        c.execute(
            """
            INSERT
            INTO    customers(username, first_name, last_name, password)
            VALUES  (?, ?, ?, ?)
            """,
            [credentials["username"],
             credentials["fullName"].split()[0],
             credentials["fullName"].split()[1],
             credentials["pwd"]]
        )
        response.status = 201
        return f"http://localhost:7007/users/{credentials['username']}"
    except sqlite3.IntegrityError as e:
        response.status = 400
        return f"Username already exists."
    except sqlite3.ProgrammingError as e:
        response.status = 400
        return f"Bad input."
    except sqlite3.DatabaseError as e:
        response.status = 400
        print("something went wrong")
        raise(e)

#
## /users/<username>/tickets
# should give a summary of all tickets for a user, like this:
# {
#     "data": [
#         {
#             "date": "2021-02-22",
#             "startTime": "19:00",
#             "theater": "Kino",
#             "title": "The Shape of Water",
#             "year": 2017,
#             "nbrOfTickets": 2
#         },
#         {
#             "date": "2021-02-23",
#             "startTime": "19:00",
#             "theater": "Skandia",
#             "title": "Moonlight",
#             "year": 2016,
#             "nbrOfTickets": 1
#         }
#     ]
# }

### /movies
## POST
# Create a new movie with a JSON-request such as this one:
#
# {
#     "imdbKey": "tt4975722",
#     "title": "Moonlight",
#     "year": 2016
# },
#
# If the IMDb key is taken, return 400, otherwise return /movies/<imdbKey> in a 201
@post("/movies")
def users():
    movie_details = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO    movies(imdb_key, title, year)
            VALUES  (?, ?, ?)
            """,
            [movie_details["imdbKey"],
             movie_details["title"],
             movie_details["year"]]
        )
        response.status = 201
        return f"http://localhost:7007/movies/{movie_details['imdbKey']}"
    except sqlite3.IntegrityError as e:
        response.status = 400
        return f"Movie already exists."
    except sqlite3.ProgrammingError as e:
        response.status = 400
        return f"Bad input."
    except sqlite3.DatabaseError as e:
        response.status = 400
        print("something went wrong")
        raise(e)

@post("/performances")
def performances():
    performance_details = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO    screenings(imdb_key, t_name, start_date, start_time)
            VALUES  (?, ?, ?, ?)
            RETURNING screening_id;
            """,
            [performance_details["imdbKey"],
             performance_details["theater"],
             performance_details["date"],
             performance_details["time"]]
        )
        found = c.fetchone()

        if not found:
            response.status = 400
            return "Illegal input."
        else:
            db.commit()
            response.status = 201
            screening_id, = found
            return f"http://localhost:7007/performances/{screening_id}"

    except sqlite3.IntegrityError as e:
        response.status = 400
        return f"Performances already exists."
    except sqlite3.ProgrammingError as e:
        response.status = 400
        return f"Bad input."
    except sqlite3.DatabaseError as e:
        response.status = 400
        print("something went wrong")
        raise(e)
    return

@route('/movies')
def get_movies():
    query = """
        SELECT *
        FROM movies
        WHERE 1=1
    """
    params = []
    if request.query.title:
        query += " AND title = ? "
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND year = ? "
        params.append(unquote(request.query.year))

    c = db.cursor()
    c.execute(query, params)

    found = [{"imdbKey": imdb_key, "title": title, "year": year}
    for year, title, imdb_key in c]

    response.status = 200

    return {"data": found}

# should give information about the movie with the given IMDB-key
#
## /movies\?title=Moonlight
# {
#     "data": [
#         {
#             "imdbKey": "tt4975722",
#             "title": "Moonlight",
#             "year": 2016
#         },
#         {
#             "imdbKey": "tt0097045",
#             "title": "Moonlight",
#             "year": 1989
#         }
#     ]
# }

## /movies\?title=Moonlight\&year=2016
# {
#     "data": [
#         {
#             "imdbKey": "tt4975722",
#             "title": "Moonlight",
#             "year": 2016
#         }
#     ]
# }
# Beware that we can’t send spaces in our query strings, we need to URLencode
# them first

## /movies/<imdb-key>
## GET
# return
# {
#     "data": [
#         {
#             "performanceId": "397582600f8732a0ba01f72cac75a2c2",
#             "date": "2021-02-22",
#             "startTime": "19:00",
#             "title": "The Shape of Water",
#             "year": 2017,
#             "theater": "Kino",
#             "remainingSeats": 10
#         },
#
#     ]
# }

### /tickets
## POST
# should try to let <username> buy a ticket for <performance-id>, using the
# password <pwd>.
#
# {
#      "username": <username>,
#      "pwd": <pwd>,
#      "performanceId": <performance-id>
# }
#
# If the order is OK, i.e., there is such a performance, there is a user with
# the given username and password, and there are still free seats, the server
# should add the new ticket, set the return status to 201, and return the name
# of its new resource, which could be something like:
# /tickets/9cd452e81be30858c8597245682255db
#
# Otherwise:
#   - If there are no free seats left, the server should return the string "No
#     tickets left" and return status 400.
#
#   - If there is no such user, or if the password is wrong, the server should
#     return the string "Wrong user credentials" and the status 401.
#
#   - If something else goes astray, the server should return the annoyingly
#     vague error message "Error" and a status of 400.
#

run(host='localhost', port=7007, debug=True)
