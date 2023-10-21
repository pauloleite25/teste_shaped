from django.urls import path
from news.views import NewsAPIView, LinkAPIView

urlpatterns = [
    path("news/", NewsAPIView.as_view(), name="news-api"),
    path("news/<int:pk>/", NewsAPIView.as_view(), name="news-api-detail"),
    path("link/", LinkAPIView.as_view(), name="link-api"),
    path("link/<str:link_hash>/", LinkAPIView.as_view(), name="link-api-detail"),
]
