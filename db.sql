CREATE TABLE tracker_type (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	datatype varchar
);

CREATE TABLE tracker (
	id integer PRIMARY KEY AUTOINCREMENT,
	name varchar,
	description varchar,
	tracker_type integer,
    FOREIGN KEY (tracker_type) REFERENCES tracker_type(id)
);

CREATE TABLE tracker_logs (
	id integer PRIMARY KEY AUTOINCREMENT,
	tracker_id integer,
	timestamp datetime,
	value varchar,
	note varchar,
    FOREIGN KEY (tracker_id) REFERENCES tracker(id)
);

CREATE TABLE login_data (
	username varchar,
	name varchar,
	password varchar
);

CREATE TABLE website_data (
	name varchar,
	value varchar
);

CREATE TABLE settings (
	tracker_id integer,
	value varchar,
    PRIMARY KEY (tracker_id, value),
    FOREIGN KEY (tracker_id) REFERENCES tracker(id)
);







