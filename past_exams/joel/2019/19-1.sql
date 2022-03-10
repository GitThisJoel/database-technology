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
    class_id     TEXT, -- glöm inte detta!!
    semester     TEXT,
    course_code  TEXT,
    lucat        TEXT,
    PRIMARY KEY(class_id),
    FOREIGN KEY course_code REFERENCES course(course_code),
    FOREIGN KEY lucat REFERENCES teacher(lucat)
);

DROP TABLE IF EXISTS exercise;
CREATE TABLE exercise (
    exercise_id    TEXT,
    exercise_name  TEXT,
    decription     TEXT,
    duration       REAL,
    course_code    TEXT,
    course_name    TEXT,
    credit         REAL,
    PRIMARY KEY(exercise_id)
    FOREIGN KEY course_code REFERENCES course(course_code)
);

DROP TABLE IF EXISTS session;
CREATE TABLE session (
    session_id     TEXT,
    start_time     REAL,  
    exercise_id    TEXT,
    decription     TEXT,
    duration       REAL,
    class_id       TEXT,
    PRIMARY KEY (session_id)
    FOREIGN KEY exercise_id REFERENCES exercise(exercise_id)
    FOREIGN KEY class_id REFERENCES class(class_id)
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
    session_id  REAL,  
    stil_id     TEXT,
    PRIMARY KEY(session_id, stil_id),
    FOREIGN KEY session_id REFERENCES semester(session_id),
    FOREIGN KEY stil_id REFERENCES ta(stil_id)
);

DROP TABLE IF EXISTS session_room;
CREATE TABLE session_room (
    session_id  TEXT,  
    room_id     TEXT,
    PRIMARY KEY(session_id, room_id),
    FOREIGN KEY session_id REFERENCES semester(session_id),
    FOREIGN KEY room_id REFERENCES room(room_id)
);