CREATE DATABASE IF NOT EXISTS Showrunner;
USE Showrunner;

CREATE TABLE User(
  id VARCHAR(255),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  profile_pic VARCHAR(255),
  password_hash VARCHAR(255),
  PRIMARY KEY(id)
);

CREATE TABLE Artist(
	artist_name VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY
);

CREATE TABLE Concert(
	concert_id int4  AUTO_INCREMENT NOT NULL PRIMARY KEY,
    date DATE NOT NULL,
    location VARCHAR(255),
    artist_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (artist_name) REFERENCES Artist(artist_name) ON DELETE CASCADE
);

create TABLE Song(
	song_name VARCHAR(255),
    artist_name VARCHAR(255),
    FOREIGN KEY (artist_name) REFERENCES Artist(artist_name) ON DELETE CASCADE,
    PRIMARY KEY(artist_name, song_name)
);

CREATE TABLE UserSearches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userID varchar(255) NOT NULL,
    search_data JSON,
    search_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(id)
);

CREATE TABLE Friends(
    id1 VARCHAR(255),
    id2 VARCHAR(255),
    CHECK(id1 <> id2),
    FOREIGN KEY (id1) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (id2) REFERENCES User(id) ON DELETE CASCADE,
	PRIMARY KEY(id1, id2)
);
