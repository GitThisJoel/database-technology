SELECT start_time, room_name
FROM   session_room
JOIN   session
USING  session_id
JOIN   class
USING  (class_id)
JOIN   course
USING  (course_code)
WHERE  course_name = "Databasteknik" AND 
       semester = "2019-vt1"
ORDER BY start_time, room_name