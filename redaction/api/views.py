from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from reviews.models import Review
from api.permissions_for_types import IsAuthor, IsRedactor, IsReviewer
from rest_framework.permissions import IsAuthenticated
from problems.models import Problem
from articles.models import Article
from users.models import User 
from articles.serializers import Article_serializer
from problems.serializers import Problem_serializer
from reviews.serializers import Review_serializer
import base64

class Article_list_api(ListAPIView):
    queryset = Article.objects.filter(status = 'PUB')
    serializer_class = Article_serializer

class Article_list_api_author(ListAPIView):
    permission_classes = (IsAuthor,)
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.filter(author = request.user)
        return Response({'articles': Article_serializer(queryset, many=True).data})

class Article_list_api_redactor(ListAPIView):
    permission_classes = (IsRedactor,)
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.filter(redactor = request.user, status = 'RED1')
        return Response({'articles': Article_serializer(queryset, many=True).data})

class Article_list_api_reviewer(ListAPIView):
    permission_classes = (IsReviewer,)
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.filter(reviewer = request.user, status = 'REV1')
        return Response({'articles': Article_serializer(queryset, many=True).data})
    
class Create_article(APIView):
    permission_classes = (IsAuthor,)
    def get(self, request):
        queryset = Article.objects.filter(title = request.data['title'])
        return Response({'articles': Article_serializer(queryset, many=True).data})
    
    def post(self, request):
        queryset = Article.objects.filter(title = request.data['title'])
        if len(queryset)==0:
            art = Article.objects.create(
                title = request.data['title'],
                author = User.objects.get(id = request.user),
                path = base64.b64encode(request.data['path'].read()).decode('utf-8'),
                redactor = User.objects.filter(role = 'Redactor').order_by('?')[0]
            )
            art.save()
            return Response({'article': model_to_dict(art)})

    def patch(self, request):
        queryset = Article.objects.filter(title = request.data['title'])
        if len(queryset)>0:
            # return Response({'article': Article_serializer(queryset, many=True).data})
            art = queryset[0]
            if art.status not in ['PU', 'AG1']:
                art.path =  base64.b64encode(request.data['path'].read()).decode('utf-8') 
                art.save()
                probs = Problem.objects.filter(article = art.id)
                probs.delete()
                return Response({'article': Article_serializer(Article.objects.filter(title = request.data['title']), many=True).data})
            # pass



class Create_problem(APIView):
    permission_classes = (IsRedactor,)
    def post(self, request):
        queryset = Article.objects.filter(title = request.data['title'])
        text = request.data['text']
        art = queryset[0]
        red = request.user
        pr = Problem(text = text, article = art, redactor = red)
        pr.save()
        return Response({'problem': model_to_dict(pr)})

class List_of_problems(APIView):
    permission_classes = (IsRedactor, IsAuthor)
    def get(self, request):
        art = Article.objects.filter(title = request.data['title'])[0]
        problems = Problem.objects.filter(article = art)
        return Response({'problems': Problem_serializer(problems, many = True).data})
        
class Send_article_to_reviewer(APIView):
    permission_classes = (IsRedactor,)
    def get(self, request):
        art = Article.objects.filter(id = request.data['article'])[0]
        art.send_to_reviewer()
        problems = Problem.objects.filter(article = art)
        problems.delete()
        redactors = User.objects.filter(role = 'Reviewer').order_by('?')[0]
        art.reviewer = redactors
        art.save()
        return Response({'article': model_to_dict(art)})

class List_of_reviews_of_article(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Review.objects.filter(reviewer = request.user, article = request.data['review'])
        return Response({'reviews': Review_serializer(queryset, many=True).data})

class Send_review(APIView):
    permission_classes = (IsReviewer,)
    def post(self, request, *args, **kwargs):
        rev = Review.objects.create(
            path = base64.b64encode(request.data['path'].read()).decode('utf-8'),
            reviewer = request.user,
            article = request.data['article']
        )
        rev.save()
        return Response({'review': model_to_dict(rev)})

class Agree_article(APIView):
    permission_classes = (IsAuthor,)
    def post(self, request, *args, **kwargs):
        art = Article.objects.filter(title = request.data['title'])[0]
        art.status = 'AG1'
        art.save()
        return {'article': model_to_dict(art)}

class Profile_data(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({'user_data':model_to_dict(user)})


class Profile_update(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self, request):
        user = User.objects.filter(username = request.user.username)[0]
        fields = ['username', 
              'first_name',
              'last_name'
              ,'title', 
              'image']
        if 'username' in request.data['username'] and len(request.data['username'])>0:
            user.username = request.data['username']
        if 'first_name' in request.data['first_name'] and len(request.data['first_name'])>0:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data['last_name'] and len(request.data['last_name'])>0:
            user.last_name = request.data['last_name']
        if 'title' in request.data['title'] and len(request.data['title'])>0:
            user.title = request.data['title']
        if 'impage' in request.data['impage'] and len(request.data['impage'])>0:
            user.impage = base64.b64encode(request.data['impage'].read()).decode('utf-8'),
        user.save()
        return Response({'user_data':model_to_dict(user)})


