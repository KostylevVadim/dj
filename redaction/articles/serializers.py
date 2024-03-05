from rest_framework import serializers
from articles.models import Article

class Article_serializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field= 'username', read_only = True)
    redactor = serializers.SlugRelatedField(slug_field= 'redactor', read_only = True)
    reviewer = serializers.SlugRelatedField(slug_field= 'reviewer', read_only = True)
    
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = '__all__'

    



