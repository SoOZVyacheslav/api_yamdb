from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import Filter
from .permissions import (AdminModeratorAuthorOnly, AdminOnly,
                          AdminUserOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ProfileSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)

HTTP_METOD_NAMES = ['get', 'post', 'head', 'delete', 'patch']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [AdminOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    http_method_names = HTTP_METOD_NAMES


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data['username']
    email = request.data['email']
    username_exists = User.objects.filter(username=username).exists()
    email_exists = User.objects.filter(email=email).exists()
    if not username_exists and not email_exists:
        User.objects.create_user(email=email, username=username)
    if not username_exists and email_exists:
        return Response(
            {'message': 'Вы не можете создать пользователя с этим email'},
            status=status.HTTP_400_BAD_REQUEST)
    if username_exists and not email_exists:
        return Response(
            {'message': 'Вы не можете создать пользователя с этим username'},
            status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(username=username)
    generator = PasswordResetTokenGenerator()
    confirmation_code = generator.make_token(user)
    User.objects.filter(username=username).update(
        confirmation_code=confirmation_code
    )
    send_mail(
        'Код подтверждения Yamdb',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    return Response(
        {
            'email': f'{email}',
            'username': f'{username}'
        },
        status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data['username']
    user = get_object_or_404(User, username=username)
    generator = PasswordResetTokenGenerator()
    if generator.check_token(user, request.data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.AllowAny])
def profile(request):
    if not request.user.is_authenticated:
        return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = ProfileSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = [AdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = Filter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminModeratorAuthorOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AdminModeratorAuthorOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
