from django import forms
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))


class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))
    email = forms.EmailField(label='Email', max_length=150,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Email'}))


class WorkoutForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter name'}))


class ExerciseForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter name'}))
    order = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Lift number',
                                                               'pattern': "\d*"}))
    workout_id = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'hidden'}))


class LogForm(forms.Form):
    date = forms.DateField(
                           widget=forms.TextInput(attrs={'class': 'form-control datepicker',
                                                         'placeholder': 'Enter date',}))
    weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Enter working weight',
                                                                'pattern': "\d*"}))
    reps = forms.CharField(max_length=100,
                           widget=forms.NumberInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Enter reps',
                                                           'pattern': "\d*"}))
    exercise_id = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'hidden'}))


class SetForm(forms.Form):
    reps = forms.CharField(max_length=5)
