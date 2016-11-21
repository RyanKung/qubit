CREATE TABLE qubit(
       id serial primary key,
       name varchar(200),
       rate integer default 1,
       body text,
       entangle varchar(200),
       mappers integer ARRAY,
       reducer integer default 0,
       created_at timestamp default now(),
       flying boolean default True,
       comment text
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
