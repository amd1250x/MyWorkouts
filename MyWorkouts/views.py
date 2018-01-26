from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from forms import *
from django.contrib.auth.models import User
from models import Workout, Exercise, Log
from django.shortcuts import redirect
from serializers import WorkoutSerializer, ExerciseSerializer, LogSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
import django_filters.rest_framework


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        workouts = Workout.objects.all().filter(owner=request.user)
        exercises = Exercise.objects.all().filter(owner=request.user)
        logs = Log.objects.all().filter(owner=request.user)
        form = WorkoutForm()
        form2 = ExerciseForm()
        form3 = LogForm()
        today = datetime.datetime.today().strftime('%Y-%m-%d')
    else:
        return render(request, 'index.html')
    return render(request, 'index.html', {'workouts': workouts,
                                          'exercises': exercises,
                                          'logs': logs,
                                          'form': form,
                                          'form2': form2,
                                          'form3': form3,
                                          'today': today})


def login(request):
    errors = ""
    if request.user.is_authenticated():
        return redirect(index)
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)
            # log user in and redirect
            try:
                auth_login(request, user)
            except:
                errors += "Bad login"
                return render(request, 'registration/login.html', {'form': form,
                                                                   'errors': errors})
            return redirect(index)
        else:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(index)


def new_user(request):
    if request.user.is_authenticated():
        return redirect(index)
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if form.is_valid():
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect(index)
    else:
        form = CreateUserForm()
    return render(request, 'registration/new_user.html', {'form': form})


def add_exercise(request, workout):
    if not request.user.is_authenticated():
        return redirect(index)
    elif request.method == 'POST':
        form = ExerciseForm(request.POST)
        name = request.POST['name']
        if form.is_valid():
            e = Exercise(name=name,
                         owner=request.user,
                         workout=Workout.objects.get(id=workout))
            e.save()
            return redirect(index)
        else:
            print(form.errors)
    else:
        form = ExerciseForm()
    return render(request, 'add_exercise.html', {'form': form})


def add_workout(request):
    if not request.user.is_authenticated():
        return redirect(index)
    elif request.method == 'POST':
        form = WorkoutForm(request.POST)
        name = request.POST['name']
        if form.is_valid():
            w = Workout(name=name,
                        owner=request.user)
            w.save()
            return redirect(index)
    else:
        form = WorkoutForm()
    return render(request, 'add_workout.html', {'form': form})


def add_log(request, exercise):
    if not request.user.is_authenticated():
        return redirect(index)
    elif request.method == 'POST':
        form = LogForm(request.POST)
        date = request.POST['date']
        weight = request.POST['weight']
        reps = request.POST['reps']

        # Organize reps based on set_num

        if form.is_valid():
            log = Log(owner=request.user,
                      exercise=Exercise.objects.get(id=exercise),
                      date=date,
                      weight=weight,
                      reps=reps)
            log.save()
            return redirect(index)
    else:
        form = LogForm()
    return render(request, 'add_log.html', {'form': form})


def add_set(request, log):
    if not request.user.is_authenticated():
        return redirect(index)
    elif request.method == 'POST':
        form = SetForm(request.POST)
        reps = request.POST['reps']

        if form.is_valid():
            log = Log.objects.get(id=log)
            if log.reps == '':
                log.reps += reps
            else:
                log.reps = log.reps + "-" + reps
            log.save()
            return redirect(index)
    else:
        form = LogForm()
    return render(request, 'add_set.html', {'form': form})


def rem_set(request, log):
    if not request.user.is_authenticated():
        return redirect(index)
    else:
        x = Log.objects.get(id=log)
        temp = x.reps.split('-')
        print temp
        temp = temp[:len(temp)-1]
        print temp
        s = ""
        for i in range(len(temp)):
            s += temp[i] + "-"
        s = s[:len(s)-1]
        x.reps = s
        x.save()
        return redirect(index)


class WorkoutList(generics.ListCreateAPIView):
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        return Workout.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        return Workout.objects.all().filter(owner=self.request.user)


class ExerciseList(generics.ListCreateAPIView):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all().filter(owner=self.request.user)




class LogList(generics.ListCreateAPIView):
    serializer_class = LogSerializer

    def get_queryset(self):
        return Log.objects.all().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LogSerializer

    def get_queryset(self):
        return Log.objects.all().filter(owner=self.request.user)
