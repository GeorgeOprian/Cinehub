from cinehub_backend.models import Movie
from cinehub_backend.models import Running_movies
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import pprint
# Create your views here.

def home(request):
    return render(request, 'home.html', {'name' : "George"})

def add(request):

    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])

    res = val1 + val2

    return render(request, 'result.html', {'result': res})



#merge cu obiect de return in java
def get_movies(request): #basic get
    print ("Am primit un get ")
    
    runnings = Running_movies.objects.all()
    list_of_movies = []
    for running in runnings:
        movie_dto = create_movie_dto(running.movie.__dict__, running.__dict__)
        list_of_movies.append(movie_dto)

    resp = {}
    resp['ListOfMovies'] = list_of_movies
    
    print (resp)
    return JsonResponse(resp)

def add_movie(request): #basic post
    print("am primit un post")
    received_json_data = json.loads(request.body)
    
    print(received_json_data)
    
    movie_model = create_movie_model(received_json_data)
    print("##############################")
    print ("Movie received: ", movie_model.__dict__)
    print("##############################")
    running_movie_model = create_running_movie_model(received_json_data)
    
    movie_model.save()
    running_movie_model.save()
    
    with open('Movie.json', 'w') as outfile:
        json.dump(received_json_data, outfile)
    print (received_json_data)
    resp = {"resp":"movie added succesfully"} 
    return JsonResponse(resp)




#objects to be sent to the client
def create_movie_dto(movie, running):
    movie_dto = {}
    movie_dto["ImdbID"] = movie['imdb_id']
    movie_dto['Title'] = movie['title']
    movie_dto['Released'] = movie['released']
    movie_dto['Duration'] = movie['duration']
    movie_dto['Genre'] = movie['genre']
    movie_dto['Director'] = movie['director']
    movie_dto['Writer'] = movie['writer']
    movie_dto['Actors'] = movie['actors']
    movie_dto['Plot'] = movie['plot']
    movie_dto['Language'] = movie['language']
    movie_dto['Awards'] = movie['awards']
    movie_dto['Poster'] = movie['poster']
    movie_dto['imdbRating'] = movie['imdb_rating']

    movie_dto['RunningDate'] = running['date']
    movie_dto['RunningTime'] = running['time']
    movie_dto['HallNumber'] = running['hall_id']

    return movie_dto

#objects to be used by the data base

def create_movie_model (rec_data):
    movie = Movie(
                imdb_id = rec_data['ImdbID'],
                title = rec_data['Title'],
                released = rec_data['Released'],
                duration = rec_data['Duration'],
                genre = rec_data['Genre'],
                director = rec_data['Director'],
                writer = rec_data['Writer'],
                actors = rec_data['Actors'],
                plot = rec_data['Plot'],
                language = rec_data['Language'],
                awards = rec_data['Awards'],
                poster = rec_data['Poster'],
                imdb_rating = rec_data['imdbRating']
            )
    return movie

def create_running_movie_model(rec_data):
    running_movie = Running_movies(
                        date = rec_data['RunningDate'],
                        time = rec_data['RunningTime'],
                        imdb_id = rec_data['ImdbID'],
                        hall_id = rec_data['HallNumber']
                    )

    return running_movie


