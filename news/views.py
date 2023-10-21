from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from news.models import News, Link
from news.serializers import NewsSerializer, LinkSerializer
from rest_framework.pagination import PageNumberPagination


class NewsAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = PageNumberPagination

    def get(self, request, pk=None) -> Response:
        if pk:
            news = News.objects.get(pk=pk)
            serializer = NewsSerializer(news, many=False)
        else:
            news = News.objects.all().order_by('-created_at')
            page = self.pagination_class().paginate_queryset(news, request, view=self)
            serializer = NewsSerializer(page, many=True)

        return Response(serializer.data)

    def post(self, request) -> Response:
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        news_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LinkAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request) -> Response:
        pk = request.data.get('id', None)
        if pk:
            news = News.objects.get(pk=pk)
            link = Link.objects.create_link(news=news)
            serializer = LinkSerializer(data=link)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, link_hash=None) -> Response:
        if link_hash:
            try:
                link_data = Link.objects.get(hash_link=link_hash)
                if link_data.expiration > timezone.now():
                    news = link_data.news
                    serializer = NewsSerializer(news, many=False)
                    return Response(serializer.data)
                else:
                    raise APIException('Link Expirado ou inválido.', code=status.HTTP_400_BAD_REQUEST)
            except:
                raise APIException('Link Expirado ou inválido.', code=status.HTTP_400_BAD_REQUEST)
