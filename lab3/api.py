from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

@route('/ping')
def ping():
    return "pong"

@route('/bing_bong')
def bing_bong():
    return "fuck ya life, BING BONG!"

### /ping
## GET
# should return pong and status 200

### /reset
## POST
# empties the database, and enters the following theaters:
#
#    “Kino”, 10 seats
#    “Regal”, 16 seats
#    “Skandia”, 100 seats

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
# If the IMDb key is taken, return 400, otherwise return /users/<imdbKey> in a 201
#
## GET
# Return movies in the database in the following format:
# {
#    "data": [
#        {
#            "imdbKey": "tt5580390",
#            "title": "The Shape of Water",
#            "year": 2017
#        },
#        {
#            "imdbKey": "tt4975722",
#            "title": "Moonlight",
#            "year": 2016
#        },
#        ...
#    ]
# }
#
## /movies/<imdb-key>
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
#
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
#
# /performances
## POST
# Create a new movie with a JSON-request such as this one:
# {
#       "imdbKey": "tt5580390",
#       "theater": "Kino",
#       "date": "2021-02-22",
#       "time": "19:00"
# }
#
# This should add a new performance of a given movie, at a given theater, at a
# given date and time – we won’t bother checking for overlapping performances
# etc., if the movie and theater exist, we add the performance to our database,
# no matter what time it is scheduled for.
#
# The server should give each performance a unique id, and it should return the
# resource for the new performance (as a simple string), so a successful call
# should get a status code of 201, and a string such as:
#
# /performances/bfd3c03b041173ab1e45a6032a163418
#
# If either the movie or theater is missing in our database, we just return the
# string "No such movie or theater", and the status code 400.
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
