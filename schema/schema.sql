CREATE TABLE spout(
       id serial primary key,
       name varchar(200) unique,
       body text,
       created_at timestamp default now(),
       active boolean default True,
       rate integer default 1,
       flying boolean default False
);

CREATE TABLE qubit(
       id serial primary key,
       name varchar(200),
       entangle varchar(200),
       mappers integer ARRAY,
       reducer integer default 0,
       created_at timestamp default now(),
       flying boolean default True
);

CREATE TABLE states(
       id serial,
       ts timestamp default now(),
       qubit integer,
       index text default 'data',
       datum json default '{"data": 0}',
       tags text default '',
       primary key (qubit, ts)
);
