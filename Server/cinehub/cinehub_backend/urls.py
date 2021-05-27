from django.urls import path


from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('add',views.add, name='add'),
    path('all_movies',views.get_movies, name='get_movies'),
    path('add_movie',views.add_movie, name='add_movie')

]