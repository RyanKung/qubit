CREATE TABLE mapper(
       id serial primary key,
       name varchar(200) default 'lambda',
       side_effect bool default False,
       closure integer default 0,
       body text,
       created_at timestamp default now()
);

CREATE TABLE reducer(
       id serial primary key,
       name varchar(200) default 'lambda',
       side_effect boolean default False,
       closure integer default 0,
       body text,
       created_at timestamp default now()
);

CREATE TABLE closure(
    id serial primary key,
    closure json default '{}'
);

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
       timestamp timestamp default now(),
       qubit integer,
       datum json default '{}',
       tags text default '',
       primary key (qubit, timestamp)
);
