drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    title string not null,
    text string not null,
    users_id integer,
    foreign key(users_id) REFERENCES users(id)
);
create table users (
    id integer primary key autoincrement,
    username string not null,
    password string not null
);

