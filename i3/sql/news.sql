DROP TABLE IF EXISTS news;
CREATE TABLE news(
    pid integer primary key autoincrement,
    title string not null,
    contents string not null,
    poster_uid integer,
    time_posted integer
);
DROP TABLE IF EXISTS news_read_map;
CREATE TABLE news_read_map(
    mapid integer primary key autoincrement,
    uid integer,
    pid integer
);

