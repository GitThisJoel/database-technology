# Things to remember

## Joins

### Cross join
Joins all combinations of rows from each of `a` and `b`, the rows will contain all attributes from both tables.

```sql
SELECT     * 
FROM       a
CROSS JOIN b
```

However, we can use a `WHERE` to specify which values to join on:
```sql
SELECT     * 
FROM       a
CROSS JOIN b
WHERE      a.foo = b.bar
```

### Inner join: 
The default joining method and can be written only using `JOIN`. 
It works by joining two tabels only when two rows 'match' each other. 
Better than `CROSS JOIN` because it consumes less memory.

```sql
SELECT     * 
FROM       a
INNER JOIN b
ON         a.foo = b.bar -- join predicate (not ON), somtimes called equi-join
```

If the join predicate is a equi-join then we have
```sql
SELECT     * 
FROM       a
INNER JOIN b
USING      (foo)
```

### Left outer join: 
An inner join combines rows in different tables when there is a match in the other table, rows with no corresponding row in the other table will not turn up in the joined table.
With an outer join we can make sure that every row in one or both of the tables turn up in the joined table -- in case there is no match, it will be paired with a row containing unly `NULL` values

```sql
SELECT           *
FROM             a
LEFT OUTER JOIN  b
USING            (foo)
```

### Right outer join: 
Now, the opposite problem, we want to see applications with no matching students -- of course we could just swap students and applications in the query above, but we could also use a right outer join.

```sql
SELECT     s_name, s_id, c_name, major
FROM       students
RIGHT JOIN applications 
USING      (s_id)
```

### Full outer join: 
There is also a full outer join, which combines the left- and the right outer joins.

```sql
SELECT    s_name, s_id, c_name, major
FROM      students
FULL JOIN applications 
USING     (s_id)
```

## `HAVING`, `WHERE` and `ON` 
- Having: after `GROUP BY`
- [Read more](https://www.tutorialspoint.com/difference-between-where-and-having-clause-in-sql)
```sql
SELECT column1, column2
FROM table1, table2
WHERE [ conditions ]
GROUP BY column1, column2
HAVING [ conditions ]
ORDER BY column1, column2
```


## `UPDATE` and `INSERT`
Work by
```sql
UPDATE table 
SET colums = new value 
WHERE some condition
```

Remember that the condition can be something like 
```sql
column IN (
    SELECT column
    FROM another_table
    WHERE ... -- and so on
)
```

Insert:
```sql
INSERT
INTO    table(column1, column1, ..., columnN)
VALUES  (value1_1, value2_1, ..., valueN_1),
        (value1_2, value2_2, ..., valueN_2),
        (value1_3, value2_3, ..., valueN_3),;
```

## Default NULL to someting
Can use `coalesce` that return the first non-null value in a list: 
`coalesce(sum(cost), 0)` would return `0` if `sum(cos)` is `NULL`.

## Default id
If an id is not provided a defaultrandom value can be created
```sql
DEFAULT(lower(hex(randomblob(16)))
```

## Triggers
[Read about triggers](https://www.sqlite.org/lang_createtrigger.html)

```sql
CREATE TRIGGER trigger_name
AFTER -- BEFORE or INSTEAD OF 
INSERT ON another_table -- DELETE or UPDATE
BEGIN 
    -- below is an example of INSERT, but can also be UPDATE, DELETE or SELECT
    INSERT
    INTO investments(amount, description, repair_id)
    VALUES (NEW.cost, "repair", NEW.repair_id);
END;
```

Protect a table from inserts.
```sql
DROP TRIGGER IF EXISTS protect_transfers;
CREATE TRIGGER protect_transfers
BEFORE UPDATE ON transfers
BEGIN
  SELECT RAISE (ROLLBACK, "No updates on transfers");
END;
```

### Date and `BETWEEN`
```sql
'2018-03-13' BETWEEN start_date AND finish_date;
```