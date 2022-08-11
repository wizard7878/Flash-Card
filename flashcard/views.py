from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .permissions import ListUserPermission
from core.models import Category, User, Word
from .serializer import (
    CategorySerializer,
    UserSerializer,
    WordSerializer,
    WordDetailSerializer
)
# Create your views here.

class CategoryApiViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin):
    """
    Category api viewset can build delete and list the user's categories
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        telegram_user_id = self.kwargs['telegram_user_id']
        return self.queryset.filter(user__telegram_user_id=telegram_user_id)
    
    def perform_create(self, serializer):
        telegram_user_id = self.kwargs['telegram_user_id']
        user = User.objects.get(telegram_user_id=telegram_user_id)
        return Category.objects.create(user= user, title=self.request.data['title'])



class UserApiViewSet(ViewSet, CreateAPIView):
    """
     User Api view can create and retrieve existsing users
     for retrieving should use telegram user id
     """
    serializer_class = UserSerializer

    def retrieve(self, request, pk):
        queryset = get_object_or_404(User, telegram_user_id=pk)
        print(queryset)
        serializer = UserSerializer(queryset, many=False)
        return Response(serializer.data)


class WordCreateApiView(CreateAPIView):
    """
    Word api can create words
    with data for example user, category
    english and persian word
    """
    serializer_class = WordSerializer


    
class WordListDeleteApiViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin):
    """
    Word List Delete viewset
    can list and delete user's word
    for list the word we can set 
    special categories or list them all
    """
    serializer_class = WordDetailSerializer
    queryset = Word.objects.all()

    def get_queryset(self):
        telegram_user_id = self.kwargs['telegram_user_id']
        try:
            categories = dict(self.request.GET).get('categories')[0].split(',')
            return self.queryset.filter(category__title__in=categories).\
                                filter(user__telegram_user_id=telegram_user_id)
        except:
            return self.queryset.filter(user__telegram_user_id=telegram_user_id)



