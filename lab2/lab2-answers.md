# Lab 2

## Which relations have natural keys?
Both `Movie` and `Theater` have natural keys.  Maybe `Customer`'s username could
be counted.

## Is there a risk that any of the natural keys will ever change?
A `Theater` can change name.  Perhaps a `Customer` could change their username.

## Are there any weak entity sets?
`Screening`s have no natural keys, only foreign ones.  `Ticket`s don't have a
natural key either, but use a invented key.

## In which relations do you want to use an invented keys? Why?
For `Ticket`s we have no other way to keep track of tickets.  It let's us keep
track of what tickets we have sold and can therefore verify if a ticket is
valid.

For `Screenings`, unless we have an invented key, its only key is all of its
attributes, including its foreign keys. 

## UML diagram
![UML diagram](uml.svg)

## Relational model
```
theater(_name_, capacity)
screening(_screening_id_, start_date, start_time, /t_name/, /m_title/, /m_year/)
tickets(_ticket_id_, /screening_id/, /username/)
movie(_year_, _title_, imdb_key, running_time)
customer(_username_, password, first_name, last_name)
```
## Describe two ways of keeping track of number of seats available.
1. Compare the capacity of the theater with the number tickets for a screening.
   This is nice because it's robust.
2. Add a variable to the screening that keeps track of the number of seats for a
   screen.
   We save a fraction of a millisecond when we retrieve the number of seats. We
   lose it when we update the number of seats.
   
