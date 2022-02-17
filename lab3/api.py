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

    c.execute("PRAGMA foreign_keys = true;")
    
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
def movies():
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
        SELECT imdb_key, title, year
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

@route('/movies/<imdb_key>')
def get_movie(imdb_key):
    c = db.cursor()
    c.execute("""
        SELECT imdb_key, title, year
        FROM movies
        WHERE imdb_key = ?
    """, [imdb_key])

    found = [{"imdbKey": imdb_key,
              "title": title,
              "year": year}
             for year, title, imdb_key in c]

    response.status = 200

    return {"data": found}

    
@route('/performances')
def get_performances():
    c = db.cursor()
    c.execute("""
    WITH ticket_count (screening_id, tickets_sold) AS (
        SELECT screening_id, count() 
        FROM tickets
        GROUP BY screening_id
    )
  
    SELECT screening_id, start_time, start_date, t_name, title, year,
        (capacity - coalesce(tickets_sold, 0)) AS remaining 
    FROM screenings
    JOIN movies USING (imdb_key)
    JOIN theaters ON theaters.name = screenings.t_name
    LEFT JOIN ticket_count USING (screening_id)
    """)

    found = [{"performanceId": screening_id,
              "title": title,
              "year": year,
              "theater": t_name,
              "date": start_date,
              "startTime": start_time,
              "remainingSeats": remaining
              }
             for screening_id,
                 title,
                 year,
                 t_name,
                 date,
                 start_time,
                 remaining in c]
    
    response.status = 200

    return {"data": found}
    


run(host='localhost', port=7007, debug=True)
