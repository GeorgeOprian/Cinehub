from types import coroutine

from django.db.models.fields import NullBooleanField
from cinehub_backend.models import Booking, Movie
from cinehub_backend.models import Running_movie
# from cinehub_backend.models import Reserved_Seat
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import json
from datetime import datetime
# Create your views here.

RESP_CODE_SUCCES = 200
RESP_CODE_COULD_NOT_INSERT_IN_DB = 512
RESP_CODE_BOOKINGS_LINKED_TO_MOVIE = 513
RESP_CODE_RESOURCE_NOT_FOUND = 204

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
    
    runnings = Running_movie.objects.all()
    list_of_movies = []
    for running in runnings:
        movie_dto = create_movie_dto(running.movie.__dict__, running.__dict__)
        list_of_movies.append(movie_dto)

    resp = {}
    resp['ListOfMovies'] = list_of_movies
    
    print (resp)
    return JsonResponse(resp)


def get_bookings(request):
    user_id = request.GET['user_id']
    print("##############################")
    print (user_id)
    print("##############################")
    # user_id = "CAAGM8TJqxeyz4qrTr8EWfjKvJw1"
    cursor = connection.cursor()
    cursor.execute('select booking_id, title, poster, date, time, seats, user_id  from cinehub_backend_booking b '
                    + ' join cinehub_backend_running_movie r on b.running_id = r.running_id '
                    + ' join cinehub_backend_movie m on r.movie_id = m.imdb_id '
                    + ' where user_id = %s', [user_id])
    res = dictfetchall(cursor)
    
    bookings = []
    for result in res:
        bookings.append(create_booking_dto(result))
    
    resp = {}
    resp['ListOfBookings'] = bookings
    print("##############################")
    print (resp)
    return JsonResponse(resp)
    


def add_movie(request): #basic post
    print("am primit un film")
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

def add_booking(request):
    print("am primit o rezervare")
    received_json_data = json.loads(request.body)

    print("##############################")
    print(received_json_data)
    print("##############################")

    resp_code = update_running_movie_seats(received_json_data)
    if resp_code == RESP_CODE_SUCCES:
        booking_model = create_booking_model(received_json_data)
        booking_model.save()
    
    resp = {"resp":"booking added succesfully"} 
    return JsonResponse(resp, status = resp_code)

def delete_movie(request):
    resp_code = RESP_CODE_SUCCES
    movie_title = request.GET['movie_title']
    print ("Filmul pe care doritit sa-l stergeti: ", movie_title)
    movies = Movie.objects.all()
    movies_to_be_deleted = []
    movie_found = False
    for movie in movies:
        if movie_title.lower() in movie.title.lower():
            movies_to_be_deleted.append(movie)
            movie_found = True
    
    if not movie_found:
        print ("fimul nu a fost gasit")
        resp_code = RESP_CODE_RESOURCE_NOT_FOUND 
        return HttpResponse(status = resp_code)

    for movie in movies_to_be_deleted:
        runnings = Running_movie.objects.all().filter(movie_id = movie.imdb_id)
        for running in runnings:
            if len(running.occupied_seats) != 0:
                resp_code = RESP_CODE_BOOKINGS_LINKED_TO_MOVIE
                return HttpResponse(status = resp_code)

    for movie in movies_to_be_deleted:
        movie.delete()
    return HttpResponse(status = resp_code)

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

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
    print ("in create_running_movie_model ")
    print(rec_data)
    running_movie = Running_movie(
                        date = rec_data['RunningDate'],
                        time = rec_data['RunningTime'],
                        movie_id = rec_data['ImdbID'],
                        hall_id = rec_data['HallNumber']
                    )
    return running_movie


def create_booking_model(rec_data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    booking = Booking(
        seats = convert_list_of_seats_from_int_to_string(rec_data['ReservedSeats']),
        user_id = rec_data['UserId'],
        running_id = rec_data['RunningId'],
        date_time = dt_string
    )

    return booking

def update_running_movie_seats(rec_data):
    running_movie = Running_movie.objects.get(running_id = rec_data['RunningId'])
    seats_from_client = rec_data['ReservedSeats']
    print ("seats_from_client", seats_from_client)
    print ("seats_from_bd", running_movie.occupied_seats)

    resp_status = RESP_CODE_SUCCES
    for seat in seats_from_client:
        if str(seat) in running_movie.occupied_seats:
            resp_status = RESP_CODE_COULD_NOT_INSERT_IN_DB
            return resp_status
        running_movie.occupied_seats += " " + str(seat)

    print ("locuri ocupate", running_movie.occupied_seats)
    running_movie.save()
    return resp_status



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

    movie_dto['RunningId'] = running['running_id']
    movie_dto['RunningDate'] = running['date']
    movie_dto['RunningTime'] = running['time']
    movie_dto['HallNumber'] = running['hall_id']

    movie_dto['OccupiedSeats'] = convert_list_of_seats_from_string_to_int(running['occupied_seats'])

    # movie_dto['OccupiedSeats'] = select_seats_for_running(running)

    return movie_dto

def convert_list_of_seats_from_string_to_int(list_of_seats_string):
    if list_of_seats_string == '':
        return []
    list_of_parsed_seats = list_of_seats_string.split(" ")

    print ("list_of_seats_string = ", list_of_seats_string)
    print ("list_of_parsed_seats = ", list_of_parsed_seats)
    list_of_seats_ints = []    
    for seat in list_of_parsed_seats:
        if seat != "":
            list_of_seats_ints.append(int(seat))
    return list_of_seats_ints

def convert_list_of_seats_from_int_to_string(list_of_seats_int):
    if list_of_seats_int == []:
        return ""
    string_ints = [str(seat) for seat in list_of_seats_int]
    list_of_seats_string = " ".join(string_ints)
    return list_of_seats_string


def create_booking_dto (booking):
    booking_dto = {}
    booking_dto['BookingId'] = booking['booking_id']
    booking_dto['MovieTitle'] = booking['title']
    booking_dto['Poster'] = booking['poster']
    booking_dto['RunningDate'] = booking['date']
    booking_dto['RunningTime'] = booking['time']
    booking_dto['ReservedSeats'] = convert_list_of_seats_from_string_to_int(booking['seats'])

    
    return booking_dto
    
 
# def select_seats_for_running (running):
#     result = Reserved_Seat.objects.filter(running = running['running_id']).values()
#     result_list = list(result)

#     list_of_seats = []
#     for seat_obj in result_list:
#         list_of_seats.append(seat_obj['seat_number'])
    
#     return list_of_seats

#objects to be used by the data base



