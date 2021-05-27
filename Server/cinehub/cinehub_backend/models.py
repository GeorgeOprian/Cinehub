from django.db import models
from django.db.models.deletion import CASCADE


class Movie (models.Model):
    # title = models.CharField(max_length = 30)
    imdb_id = models.CharField(max_length = 10, primary_key=True)
    title = models.CharField(max_length = 100)
    released = models.CharField(max_length = 50)
    duration = models.CharField(max_length = 10)
    genre = models.CharField(max_length = 100)
    director = models.CharField(max_length = 100)
    writer = models.CharField(max_length = 500)
    actors = models.CharField(max_length = 200)
    plot = models.CharField(max_length = 500)
    language = models.CharField(max_length = 50)
    awards = models.CharField(max_length = 200)
    poster = models.CharField(max_length = 300)
    # ratings = models.CharField(max_length = 500) # adaug mai tarziu rating urile
    imdb_rating = models.CharField(max_length = 6)


def __str__(self):
    return self.imdb_id + " " + self.title + " " + self.released + " " + self.duration + " " + self.genre + " " + self.director + " " + self.writer + " " + self.actors + " " + self.plot + " " + self.language + " " + self.awards + " " + self.poster + " " + " " + self.imdb_rating 


class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    number_of_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.hall_id + " " + self.number_of_seats



class Running_movies(models.Model):
    running_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length = 12)
    time = models.CharField(max_length = 5)
    occupied_seats = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_id", "hall_id"], name="unique_movie_hall"
            ), 
            models.UniqueConstraint(
                fields=["date", "time", "hall_id"], name="unique_movie_date_time"
            )
        ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return self.running_id + " " + self.date +  " " + self.time + " " + self.occupied_seats + " " + self.movie + " " + self.hall
    


class Booking (models.Model):
    booking_id = models.AutoField(primary_key=True)
    seats = models.CharField(max_length = 200)
    user_id = models.CharField(max_length = 30)
    running = models.ForeignKey(Running_movies, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.booking_id + " " + self.seats + " " + self.user_id  + " " + self.running 
