from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('clubs/', views.clubs, name='clubs'),
    path('tag/<player_id>/', views.playerTag, name='playerTag'),
    path('clubs/<club_tag>/', views.clubTag, name='clubTag'),
    path('youtube/', views.youtube, name='youtube'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup_view, name='signup_view')

]