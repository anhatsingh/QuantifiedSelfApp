CREATE TABLE tracker_type (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar(55),
	datatype varchar(15)
);

CREATE TABLE tracker (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar(100),
	description varchar(255),
	tracker_type integer,
    FOREIGN KEY (tracker_type) REFERENCES tracker_type(id)
);

CREATE TABLE tracker_logs (
	id integer PRIMARY KEY AUTOINCREMENT,
	tracker_id integer,
	timestamp datetime,
	value varchar(255),
	note varchar(255),
    FOREIGN KEY (tracker_id) REFERENCES tracker(id)
);

CREATE TABLE user (
	id integer PRIMARY KEY AUTOINCREMENT,
	username varchar(55),
	email varchar(55),
	password varchar(255),
	active integer
);

CREATE TABLE role (
	id integer PRIMARY KEY,
	name varchar(55),
	description varchar(255)
);

CREATE TABLE roles_users (
	id INTEGER PRIMARY KEY,
	user_id integer,
	role_id integer,
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (role_id) REFERENCES role(id)
);


CREATE TABLE website_data (
	name varchar(55),
	value varchar(255)
);

CREATE TABLE settings (
	tracker_id integer,
	value varchar(255),
    PRIMARY KEY (tracker_id, value),
    FOREIGN KEY (tracker_id) REFERENCES tracker(id)
);