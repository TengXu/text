CREATE DATABASE photoshare;
USE photoshare;

CREATE TABLE Users (
  user_id int NOT NULL AUTO_INCREMENT,
  firstname VARCHAR(255),
  lastname VARCHAR(255),
  email varchar(255) UNIQUE,
  birthday DATE,
  password varchar(255) NOT NULL,
  hometown VARCHAR(255),
  gender VARCHAR(6),
	KEY (user_id),
  CONSTRAINT PRIMARY KEY (user_id)
);

CREATE TABLE Friends(
	user_id INT NOT NULL,
	friend_id INT NOT NULL,
	CONSTRAINT PRIMARY KEY(user_id, friend_id),
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY (friend_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Photo (
  photo_id int NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL ,
  photopath VARCHAR(255),
  caption VARCHAR(255),
	KEY (photo_id),
  CONSTRAINT PRIMARY KEY (photo_id),
  CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
);

CREATE TABLE Text (
  text_id int NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL ,
  content TEXT,
  caption VARCHAR(255),
  KEY (photo_id),
  CONSTRAINT PRIMARY KEY (text_id),
  CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
);

CREATE TABLE Comment(
	comment_id INT NOT NULL AUTO_INCREMENT,
	text VARCHAR(255) NOT NULL,
	datecreate TIMESTAMP NOT NULL,
	user_id INT NOT NULL,
	photo_id INT NOT NULL,
	CONSTRAINT PRIMARY KEY (comment_id),
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY (photo_id) REFERENCES Photo(photo_id) ON DELETE CASCADE
);

CREATE TABLE Tag(
	tag VARCHAR(255) NOT NULL,
  photo_id int NOT NULL ,
	CONSTRAINT PRIMARY KEY (tag),
  CONSTRAINT FOREIGN KEY (photo_id) REFERENCES Photo(photo_id) ON DELETE CASCADE
);

CREATE TABLE Likes(
	user_id INT NOT NULL,
	photo_id INT NOT NULL,
	datecreate TIMESTAMP NOT NULL,
  CONSTRAINT PRIMARY KEY (user_id, photo_id),
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY (photo_id) REFERENCES Photo(photo_id) ON DELETE CASCADE
);

CREATE TABLE Activity(
  user_id INT NOT NULL,
  activity INT,
  CONSTRAINT PRIMARY KEY (user_id),
  CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Users (email, password) VALUES ('test@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');
