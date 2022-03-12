# Things to remember

## Joins


## `HAVING`, `WHERE` and `ON` 
- Having: after `GROUP BY`
- [Link to read more](https://www.tutorialspoint.com/difference-between-where-and-having-clause-in-sql)
```
SELECT column1, column2
FROM table1, table2
WHERE [ conditions ]
GROUP BY column1, column2
HAVING [ conditions ]
ORDER BY column1, column2
```


## `INSERT`
Work by
```
UPDATE table 
SET colums = new value 
WHERE some condition
```

Remember that the condition can be something like 
```
column IN (
    SELECT column
    FROM another_table
    WHERE ... -- and so on
)
``` 

## Default NULL to someting
Can use `coalesce` that return the first non-null value in a list: 
`coalesce(sum(cost), 0)` would return `0` if `sum(cos)` is `NULL`.