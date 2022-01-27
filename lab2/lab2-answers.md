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

# UML diagram
![UML diagram](uml.svg)
