from cinehub_backend.models import Booking, Movie
from cinehub_backend.models import Running_movie
# from cinehub_backend.models import Reserved_Seat
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
    user_id = "CAAGM8TJqxeyz4qrTr8EWfjKvJw1"
    queryset = Running_movie.objects.all().select_related('running_id').select_related('imdb_id')
    print (queryset)

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
    if resp_code == 200:
        booking_model = create_booking_model(received_json_data)
        booking_model.save()
    

    
    # Running_movie.objects.filter(running_id = received_json_data['RunningId']).update(occupied_seats = convert_list_of_seats_from_int_to_string(received_json_data['ReservedSeats']))

    # running_movie = create_running_movie_for_booking(received_json_data)
    # print(running_movie.occupied_seats)
    # running_movie.save()
    
    resp = {"resp":"booking added succesfully"} 
    return JsonResponse(resp, status = resp_code)


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
    booking = Booking(
        seats = str(rec_data['ReservedSeats']),
        user_id = rec_data['UserId'],
        running_id = rec_data['RunningId']
    )

    return booking

def update_running_movie_seats(rec_data):
    running_movie = Running_movie.objects.get(running_id = rec_data['RunningId'])
    seats_from_client = rec_data['ReservedSeats']
    print ("seats_from_client", seats_from_client)
    print ("seats_from_bd", running_movie.occupied_seats)

    resp_status = 200
    for seat in seats_from_client:
        if str(seat) in running_movie.occupied_seats:
            resp_status = 512
            return resp_status
        running_movie.occupied_seats += " " + str(seat)



    print ("locuri ocupate", running_movie.occupied_seats)
    running_movie.save()
    return resp_status


# def create_list_of_seats(rec_data):
#     seat_numbers = rec_data['ReservedSeats']
#     seat_models = []
#     for seat in seat_numbers:
#         seat_models.append(Reserved_Seat(
#             running_id = rec_data['RunningId'],
#             seat_number = seat
#         ))
#     return seat_models



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
 
# def select_seats_for_running (running):
#     result = Reserved_Seat.objects.filter(running = running['running_id']).values()
#     result_list = list(result)

#     list_of_seats = []
#     for seat_obj in result_list:
#         list_of_seats.append(seat_obj['seat_number'])
    
#     return list_of_seats

#objects to be used by the data base



