-- users(user_id, username, address)
DROP TABEL IF EXISTS users;
CREATE TABLE users (

);

-- subscriptions(phone_no, user_id)
DROP TABEL IF EXISTS subscriptions;
CREATE TABLE subscriptions (

);

-- calls(call_id, caller_no, callee_no, start_time, finish_time, cost)
-- (b)
DROP TABEL IF EXISTS calls;
CREATE TABLE calls (
    call_id     TEXT,
    caller_no   TEXT,
    callee_no   TEXT,
    start_time  DATE,
    finish_time DATE,
    cost        REAL,
    PRIMARY KEY (call_id),
    FOREIGN KEY (caller_no) REFERENCES subscriptions(caller_no),
    FOREIGN KEY (callee_no) REFERENCES subscriptions(callee_no)
);

-- (c)
SELECT   caller_no, cost
FROM     calls
ORDER BY start_time 
LIMIT    10;

-- (d)
SELECT  username, address
FROM    users
JOIN    subscriptions
USING   (user_id) -- WHERE   subscriptions.user_id = users.user_id
WHERE   phone_no = "0707-123456"

-- (e)
SELECT username, address
FROM subscriptions
JOIN users
USING (user_id)
GROUP BY user_id
HAVING count(user_id) > 1; -- NOT WHERE

SELECT  username, address, sum(cost) AS total_cost
FROM    user
JOIN    subscriptions
USING   (user_id)
JOIN    calls
ON      subscriptions.phone_no = calls.caller_no -- not where
GROUP BY (user_id)
HAVING  total_cost > 1000




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
WHERE   phone_no NOT IN called_from AND NOT IN called;
--alt !! ?
WHERE   phone_no NOT IN (
            SELECT  phone_no
            FROM    called_from
        ) AND (
            SELECT  phone_no
            FROM    called  
        ) 
    )