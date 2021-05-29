from django.urls import path


from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('add',views.add, name='add'),
    path('all_movies',views.get_movies, name='get_movies'),
    path('bookings_for_user',views.get_bookings, name='get_bookings'),
    path('add_movie',views.add_movie, name='add_movie'),
    path('add_booking',views.add_booking, name='add_booking'),
    path('delete_movie',views.delete_movie, name='delete_movie')
]