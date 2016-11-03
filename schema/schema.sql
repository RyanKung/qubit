CREATE SCHEMA qubit;

CREATE TABLE mapper(
       id integer,
       name varchar(200),
       side_effect bool,
       closure json,
       body json
);

CREATE TABLE reducer(
       id integer,
       name varchar(200),
       side_effect boolean,
       closure json,
       body json
);
