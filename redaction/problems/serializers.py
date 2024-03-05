from problems.models import Problem

from rest_framework import serializers


class Problem_serializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'