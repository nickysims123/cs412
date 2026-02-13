
from django.urls import path
from .views import ShowAllView
from .views import ArticleView
from .views import RandomArticleView


urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
]