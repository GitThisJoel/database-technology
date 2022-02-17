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
@post('/reset')
def reset():
    c = db.cursor()

    c.execute("PRAGMA foreign_keys = true;")

    tables = ["tickets", "screenings", "theaters", "customers", "movies"]
    for t in tables:
        c.execute(f"DELETE FROM {t}")
        db.commit()

    c.execute(
        """
        INSERT
        INTO theaters(name, capacity)
        VALUES ("Kino", 10),
               ("Regal", 16),
               ("Skandia", 100);
        """
    )
    db.commit()
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

        db.commit()
        response.status = 201
        return f"/users/{credentials['username']}"
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
        return f"/movies/{movie_details['imdbKey']}"
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
            return f"/performances/{screening_id}"

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
    for imdb_key, title, year in c]

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
             for imdb_key, title, year in c]

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

    SELECT screenings.screening_id, start_time, start_date, t_name, title, year,
        (capacity - coalesce(tickets_sold, 0)) AS remaining
    FROM screenings
    JOIN movies USING (imdb_key)
    JOIN theaters ON theaters.name = screenings.t_name
    LEFT JOIN ticket_count ON screenings.screening_id = ticket_count.screening_id
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
                 start_date,
                 start_time,
                 remaining in c]

    response.status = 200

    return {"data": found}

@post("/tickets")
def tickets():
    c = db.cursor()
    ticket_details = request.json

    c.execute("""
        WITH has_tickets(screening_id) AS (
            SELECT screening_id
            FROM screenings
            JOIN theaters ON theaters.name = screenings.t_name
            LEFT JOIN tickets USING(screening_id) 
            GROUP BY screening_id
            HAVING (capacity - count()) > 0)
    
        SELECT *
        FROM has_tickets
        WHERE screening_id = ?
    """, [ticket_details["performanceId"]]);

    found = c.fetchone()

    if not found:
        response.status = 400
        return "No tickets left"            
    else:    
        c.execute("""
            SELECT *
            FROM customers
            WHERE username = ? AND password = ?
        """, [ticket_details["username"], ticket_details["pwd"]])
        
        found = c.fetchone()
        
        if not found:
            response.status = 401
            return "Wrong user credentials"
        else:             
            c.execute("""
                INSERT INTO tickets(username, screening_id)
                VALUES (?, ?)
                RETURNING ticket_id
            """, [ticket_details["username"], ticket_details["performanceId"]])
              
            found = c.fetchone()
                   
            if found:
                db.commit()
                response.status = 201
                t_id, = found
                return f"/tickets/{t_id}"
            else:
                response.status = 400
                return "An error occured"            

@route("/users/<username>/tickets")
def get_customer_tickets(username):
    c = db.cursor()
    c.execute("""
        SELECT start_date, start_time, t_name, title, year, count(*) as number_of_tickets
        FROM tickets
        JOIN screenings USING(screening_id)
        JOIN movies USING(imdb_key)
        WHERE username = ?
        GROUP BY screening_id
    """, [username])
    
    found = [{"date": date,
              "startTime": start_time,
              "theater": t_name,
              "title": title,
              "year": year,
              "nbrOfTickets": number_of_tickets}
             for date, start_time, t_name, title, year, number_of_tickets in c]

    response.status = 200
    return {"data": found}

run(host='localhost', port=7007, debug=True)
