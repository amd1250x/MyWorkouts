from rest_framework import serializers
from models import Workout, Exercise, Log


class WorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ('id', 'name', 'owner')


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'order', 'repsStart', 'repsEnd', 'setsStart', 'setsEnd', 'workout_id', 'owner')

    def create(self, validated_data):
        e = Exercise(name=validated_data['name'],
                     order=validated_data['order'],
                     repsStart=validated_data['repsStart'],
                     repsEnd=validated_data['repsEnd'],
                     setsStart=validated_data['setsStart'],
                     setsEnd=validated_data['setsEnd'],
                     workout_id=validated_data['workout_id'],
                     owner=validated_data['owner'])
        e.save()
        return e


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = ('id', 'exercise_id', 'date', 'weight', 'reps')

