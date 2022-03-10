DROP TABLE IF EXISTS course;
CREATE TABLE course (
    course_code  TEXT,
    course_name  TEXT,
    credit       REAL,
    PRIMARY KEY(course_code)
);

DROP TABLE IF EXISTS teacher;
CREATE TABLE teacher (
    lucat   TEXT,
    name    TEXT,
    PRIMARY KEY(lucat)
);

DROP TABLE IF EXISTS class;
CREATE TABLE class (
    semester     TEXT,
    course_code  TEXT,
    lucat        TEXT,
    PRIMARY KEY(semester),
    FOREIGN KEY course_code REFERENCES course(course_code),
    FOREIGN KEY lucat REFERENCES teacher(lucat)
);

DROP TABLE IF EXISTS exercise;
CREATE TABLE exercise (
    exercise_name  TEXT,
    decription     TEXT,
    duration       REAL,
    course_code    TEXT,
    course_name    TEXT,
    credit         REAL,
    PRIMARY KEY(exercise_name)
    FOREIGN KEY course_code REFERENCES course(course_code)
);

DROP TABLE IF EXISTS session;
CREATE TABLE session (
    start_time     REAL,  
    exercise_name  TEXT,
    decription     TEXT,
    duration       REAL,
    semester       TEXT,
    PRIMARY KEY (start_time)
    FOREIGN KEY exercise_name REFERENCES exercise(exercise_name)
    FOREIGN KEY semester REFERENCES class(semester)
);

DROP TABLE IF EXISTS ta;
CREATE TABLE ta (
    stil_id  TEXT,
    PRIMARY KEY(stil_id)
);

DROP TABLE IF EXISTS room;
CREATE TABLE room (
    room_id  TEXT,
    PRIMARY KEY(room_id)
);

DROP TABLE IF EXISTS session_ta;
CREATE TABLE session_ta (
    start_time  REAL,  
    stil_id     TEXT,
    PRIMARY KEY(start_time, stil_id),
    FOREIGN KEY start_time REFERENCES semester(start_time),
    FOREIGN KEY stil_id REFERENCES ta(stil_id)
);

DROP TABLE IF EXISTS seassion_room;
CREATE TABLE seassion_room (
    start_time  REAL,  
    room_id     TEXT,
    PRIMARY KEY(start_time, room_id),
    FOREIGN KEY start_time REFERENCES semester(start_time),
    FOREIGN KEY room_id REFERENCES room(room_id)
);