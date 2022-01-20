%%sql
WITH
    ssn_avg_grade(ssn, avg_weighted_grade) AS (
        SELECT   ssn, sum(grade*credits)/sum(credits) AS "avg_weighted_grade"
        FROM     taken_courses
        JOIN     courses
        USING    (course_code)
        GROUP BY ssn
    ),
    count_names(first_name, name_count) AS (
        SELECT   first_name, count() AS name_count
        FROM     students
        GROUP BY first_name
    ),
    avg_of_all_other(first_name, avg_of_others) AS (
        SELECT   first_name, avg_of_others
        FROM     students

    )
