
CREATE DATABASE IF NOT EXISTS Showrunner;
USE Showrunner;

CREATE TABLE User(
  id VARCHAR(255),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  profile_pic VARCHAR(255) NOT NULL,
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

