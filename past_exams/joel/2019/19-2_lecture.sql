-- users(user_id, username, address)
DROP TABEL IF EXISTS users;
CREATE TABLE users (

);

-- subscriptions(phone_no, user_id)
DROP TABEL IF EXISTS subscriptions;
CREATE TABLE subscriptions (

);



-- calls(call_id, caller_no, callee_no, start_time, finish_time, cost)
DROP TABEL IF EXISTS calls;
CREATE TABLE calls (

);


-- (f)
SELECT    username, address, sun(cost) AS total_cost
FROM      calls 
JOIN      subscriptions
ON        subscriptions.phone_no = calls.caller_no
JOIN      users
USING     (user_id)
GROUP BY  user_id
HAVING    total_cost > 1000;

-- (g)
WITH 
    called_from(phone_no) AS (
        SELECT  caller_no 
        FROM    calls
    ),  
    called(phone_no) AS (
        SELECT  callee_no
        FROM    calls
    )
SELECT  phone_no
FROM    subscriptions
WHERE   phone_no NOT IN called_from AND NOT IN called
--alt !! ?
WHERE   phone_no NOT IN (
            SELECT  phone_no
            FROM    called_from
        ) AND (
            SELECT  phone_no
            FROM    called  
        ) 
    )