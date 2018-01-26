from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new_user/$', views.new_user, name='new_user'),
    url(r'^add_exercise/(?P<workout>\d+)/$', views.add_exercise, name='add_exercise'),
    url(r'^add_log/(?P<exercise>\d+)/$', views.add_log, name='add_log'),
    url(r'^add_set/(?P<log>\d+)/$', views.add_set, name='add_set'),
    url(r'^rem_set/(?P<log>\d+)/$', views.rem_set, name='rem_set'),
    url(r'^add_workout/$', views.add_workout, name='add_workout'),
    url(r'^workouts/$', views.WorkoutList.as_view(), name='workout-list'),
    url(r'^workouts/(?P<pk>[0-9]+)/$', views.WorkoutDetail.as_view(), name='workout-detail'),
    url(r'^exercises/$', views.ExerciseList.as_view(), name='exercise-list'),
    url(r'^exercises/(?P<pk>[0-9]+)/$', views.ExerciseDetail.as_view(), name='exercise-detail'),
    url(r'^logs/$', views.LogList.as_view(), name='log-list'),
    url(r'^logs/(?P<pk>[0-9]+)/$', views.LogDetail.as_view(), name='log-detail'),
]
