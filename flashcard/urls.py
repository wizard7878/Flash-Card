from django.urls import path,include
from .views import CategoryApiViewSet, UserApiViewSet, WordCreateApiView, WordListDeleteApiViewSet
from rest_framework import routers

category_router = routers.DefaultRouter()
category_router.register('category', CategoryApiViewSet, basename='category')

word_router = routers.DefaultRouter()
word_router.register('words', WordListDeleteApiViewSet, basename='words')

user_router = routers.DefaultRouter()
user_router.register('user', UserApiViewSet, basename='user')



urlpatterns = [
    path('', include(user_router.urls)),
    path('<int:telegram_user_id>/', include(category_router.urls)),
    path('create/word/', WordCreateApiView.as_view(), name='create-word'),
    path('<int:telegram_user_id>/', include(word_router.urls))
]