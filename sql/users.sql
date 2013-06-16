DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_permission_map;

CREATE TABLE user_permission_map(
    mapid integer primary key autoincrement,
    uid integer,
    permission string
);
CREATE TABLE users(
    uid integer primary key autoincrement,
    username string not null,
    passwd_hash string not null
);
insert into users (username, passwd_hash) values ("demo", "2a97516c354b68848cdbd8f54a226a0a55b21ed138e207ad6c5cbb9c00aa5aea");
insert into user_permission_map (uid, permission) values (1, "admin_news");
insert into user_permission_map (uid, permission) values (1, "admin_user");

