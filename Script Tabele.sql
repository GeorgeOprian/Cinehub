CREATE TABLE movie
(
  imdb_Id VARCHAR(10) NOT NULL,
  title VARCHAR(20) NOT NULL,
  Released VARCHAR(15) NOT NULL,
  Runtime VARCHAR(8) NOT NULL,
  Genre VARCHAR(50) NOT NULL,
  Director VARCHAR(50) NOT NULL,
  Writer VARCHAR(50) NOT NULL,
  Actors VARCHAR(100) NOT NULL,
  Plot VARCHAR(500) NOT NULL,
  Language VARCHAR(15) NOT NULL,
  Awards VARCHAR(30) NOT NULL,
  Poster VARCHAR(250) NOT NULL,
  Ratings VARCHAR(500) NOT NULL,
  imdb_rating VARCHAR(6) NOT NULL,
  PRIMARY KEY (imdb_Id)
);

CREATE TABLE hall
(
  hall_id INT NOT NULL,
  number_of_seats INT NOT NULL,
  PRIMARY KEY (hall_id)
);

CREATE TABLE running_movies
(
  running_id INT NOT NULL,
  date VARCHAR(12) NOT NULL,
  time VARCHAR(6)NOT NULL,
  occupied_seats INT NOT NULL,
  imdb_Id VARCHAR(10) NOT NULL,
  hall_id INT NOT NULL,
  PRIMARY KEY (running_id),
  FOREIGN KEY (imdb_Id) REFERENCES movie(imdb_Id),
  FOREIGN KEY (hall_id) REFERENCES hall(hall_id),
  UNIQUE (imdb_Id),
  UNIQUE (hall_id)
);

CREATE TABLE Bookings
(
  booking_id INT NOT NULL,
  seats VARCHAR(15) NOT NULL,
  user_id VARCHAR(30) NOT NULL,
  running_id INT NOT NULL,
  PRIMARY KEY (booking_id),
  FOREIGN KEY (running_id) REFERENCES running_movies(running_id)
);