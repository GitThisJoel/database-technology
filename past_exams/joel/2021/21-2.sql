-- 1)
-- employees(~employee_id~, name, hourly_wage)
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
  employee_id   TEXT,
  hourly_wage   FLOAT,
  name    TEXT,
  PRIMARY KEY(employee_id)
);

-- areas(~area_id~, size, /area_type/, /employee_id/)
DROP TABLE IF EXISTS areas;
CREATE TABLE areas (
  area_id   TEXT,
  size      FLOAT,
  area_type TEXT,
  employee_id   TEXT,
  PRIMARY KEY(area_id),
  FOREIGN KEY area_type REFERENCES area_type(area_type),
  FOREIGN KEY employee_id REFERENCES employees(employee_id)
);

-- area_types(~area_type~, work_time)
DROP TABLE IF EXISTS area_types;
CREATE TABLE area_types (
  area_type   TEXT,
  work_time   FLOAT,
  PRIMARY KEY(area_type)
);

-- 2)
SELECT   employee_id, name, hourly_wage
FROM     employees
ORDER BY name DESC

-- 3)
SELECT   area_type, sum(size)
FROM     areas
GROUP BY area_type

-- 4)
SELECT    employee_id, name
FROM      areas
JOIN      employees
USING     (employee_id)
GROUP BY  employee_id
WHERE     sum(size) IS NULL
-- maybe its right

-- correct
SELECT    employee_id, name
FROM      employees
JOIN      areas
USING     (employee_id)
WHERE     area_id IS NULL

-- 5)
SELECT   employee_id, name
FROM     areas
JOIN     employees
USING    (employee_id)
GROUP BY employee_id
WHERE    sum(size) > 1000
-- maybe correct

-- correct
SELECT    employee_id, name
FROM      employees
JOIN      areas
USING     (employee_id)
GROUP BY  employee_id
HAVING    sum(size) > 1000;

-- 6)
-- SELECT area_type, sum(work_time) -- lol I missunderstud the variable
SELECT  sum(size * work_time)
FROM    areas
JOIN    area_types
USING   (area_typer)
