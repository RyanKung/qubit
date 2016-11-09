CREATE TABLE mapper(
       id serial primary key,
       name varchar(200) default 'lambda',
       side_effect bool default False,
       closure json default '{}',
       body text,
       created_at timestamp default now()
);

CREATE TABLE reducer(
       id serial primary key,
       name varchar(200) default 'lambda',
       side_effect boolean default False,
       closure json default '{}',
       body text,
       created_at timestamp default now()
);

CREATE TABLE spout(
       id serial primary key,
       name varchar(200) default 'lambda',
       body text,
       closure json default '{}',
       created_at timestamp default now(),
       active boolean default True,
       rate integer default 1
);


CREATE TABLE qubit(
       id serial primary key,
       name varchar(200),
       entangle varchar(200),
       mappers integer ARRAY,
       reducer integer default 0,
       closure json default '{}',
       created_at timestamp default now(),
       flying boolean default True
);

CREATE TABLE states(
       id serial,
       timestamp timestamp primary key default now(),
       qubit integer,
       datum json default '{}',
       tags text default ''
);
