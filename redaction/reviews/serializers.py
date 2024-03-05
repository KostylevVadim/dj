from reviews.models import Review
from rest_framework import serializers


class Review_serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'