DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS roles_users;
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS tracker_logs;
DROP TABLE IF EXISTS tracker_type;
DROP TABLE IF EXISTS tracker;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS website_data;

CREATE TABLE role (
	id integer PRIMARY KEY,
	name varchar(55) NOT NULL,
	description varchar(255) NOT NULL
);

CREATE TABLE roles_users (
	id INTEGER PRIMARY KEY,
	user_id integer NOT NULL,
	role_id integer NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
	FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE settings (
	id integer PRIMARY KEY AUTOINCREMENT,
	tracker_id integer NOT NULL,
	value varchar(255) NOT NULL,
    FOREIGN KEY (tracker_id) REFERENCES tracker(id) ON DELETE CASCADE
);

CREATE TABLE user (
	id integer PRIMARY KEY AUTOINCREMENT,
	username varchar(55) NOT NULL,
	email varchar(55) NOT NULL,
	password varchar(255) NOT NULL,
	active integer NOT NULL
);

CREATE TABLE tracker (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar(100) NOT NULL,
	description varchar(255),
	user_id integer NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE tracker_type (
	id integer PRIMARY KEY AUTOINCREMENT,
	tracker_id integer NOT NULL,
	datatype varchar(55) NOT NULL,
	value varchar(255),
	FOREIGN KEY (tracker_id) REFERENCES tracker(id) ON DELETE CASCADE
);

CREATE TABLE tracker_logs (
	id integer PRIMARY KEY AUTOINCREMENT,
	tracker_id integer NOT NULL,
	timestamp datetime NOT NULL,
	value varchar(255) NOT NULL,
	note varchar(255),
    FOREIGN KEY (tracker_id) REFERENCES tracker(id) ON DELETE CASCADE
);

CREATE TABLE website_data (
	name varchar(55) NOT NULL PRIMARY KEY,
	value varchar(255) NOT NULL
);