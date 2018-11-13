CREATE DATABASE Justext;
USE Justext;

CREATE TABLE Users (
  user_id int NOT NULL AUTO_INCREMENT,
  username VARCHAR(255),
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

CREATE TABLE Text (
  text_id int NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL ,
  content VARCHAR(255),
  caption VARCHAR(255),
  post_time DATETIME,
	KEY (text_id),
  CONSTRAINT PRIMARY KEY (text_id),
  CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Comment(
	comment_id INT NOT NULL AUTO_INCREMENT,
	text VARCHAR(255) NOT NULL,
	datecreate TIMESTAMP NOT NULL,
	user_id INT NOT NULL,
	text_id INT NOT NULL,
	CONSTRAINT PRIMARY KEY (comment_id),
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY (text_id) REFERENCES Text(text_id) ON DELETE CASCADE
);

CREATE TABLE Likes(
	user_id INT NOT NULL,
	text_id INT NOT NULL,
	datecreate TIMESTAMP NOT NULL,
  CONSTRAINT PRIMARY KEY (user_id, text_id),
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY (text_id) REFERENCES Text(text_id) ON DELETE CASCADE
);

CREATE TABLE Activity(
  user_id INT NOT NULL,
  activity INT,
  CONSTRAINT PRIMARY KEY (user_id),
  CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
