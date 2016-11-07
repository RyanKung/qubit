CREATE SCHEMA qubit;

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
       spout text,
       closure json default '{}',
       created_at timestamp default now(),
       active boolean default True
);

CREATE TABLE qubit(
       timestamp timestamp primary key default now(),
       spout integer references spout(id),
       name varchar(200) default '',
       datum json default '{}',
       tags text default ''
);
