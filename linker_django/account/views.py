from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from .models import *
from .serializers import *
from .permissions import *

@extend_schema(
    description="Получение, обновление или удаление аккаунта по id.",
    summary="Получение, обновление или удаление аккаунта по id.",
    tags=["Account"]
)
class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LinkerUser.objects.all()
    serializer_class = LinkerUserSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        # Хешируем пароль перед сохранением
        if 'password' in self.request.data:
            user = serializer.save()  # Получаем объект пользователя
            user.set_password(self.request.data['password'])
            user.save()
        else:
            serializer.save()

@extend_schema(
    description="Получение списка всех аккаунтов или добавление нового аккаунта.",
    summary="Получение списка всех аккаунтов или добавление нового аккаунта.",
    tags=["Account"]
)
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = LinkerUser.objects.all()
    serializer_class = LinkerUserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        if 'password' in self.request.data:
            user = serializer.save()  # Получаем объект пользователя
            user.set_password(self.request.data['password'])
            user.save()
        else:
            serializer.save()
    
@extend_schema(
    description="Получение списка всех фото пользователя или добавление нового фото.",
    summary="Получение списка всех фото пользователя или добавление нового фото.",
    tags=["Account"]
)     
class AccountPhotoListCreateView(generics.ListCreateAPIView):
    queryset = LinkerUserPhoto.objects.all()
    serializer_class = LinkerUserPhotoSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return LinkerUserPhoto.objects.filter(linker_user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        linker_user = LinkerUser.objects.get(id=user_id)
        self.check_object_permissions(self.request, obj=linker_user)
        serializer.save(linker_user=linker_user)

@extend_schema(
    description="Получение или удаление фото по id.",
    summary="Получение или удаление фото по id.",
    tags=["Account"]
)
class AccountPhotoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = LinkerUserPhoto.objects.all()
    serializer_class = LinkerUserPhotoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        photo_id = self.kwargs.get('photo_id')
        linker_user = LinkerUser.objects.get(id=user_id)
        self.check_object_permissions(self.request, obj=linker_user)
        obj = get_object_or_404(LinkerUserPhoto, linker_user=linker_user, id=photo_id)  
        return obj

@extend_schema(
    description="Получение списка всех подписок пользователя или создание новой подписки.",
    summary="Получение списка всех подписок пользователя или создание новой подписки.",
    tags=["Account"]
)  
class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Subscription.objects.filter(follower=user_id)
    
    def perform_create(self, serializer):
        follower_id = self.kwargs.get('user_id')
        following_id = self.request.data['following']
        follower = LinkerUser.objects.get(id=follower_id)
        following = LinkerUser.objects.get(id=following_id)
        self.check_object_permissions(self.request, obj=follower)
        serializer.save(follower=follower, following=following)

@extend_schema(
    description="Получение или удаление подписки по id.",
    summary="Получение или удаление подписки по id.",
    tags=["Account"]
)
class SubscriptionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        subscription_id = self.kwargs.get('id')
        linker_user = LinkerUser.objects.get(id=user_id)
        self.check_object_permissions(self.request, obj=linker_user)
        obj = get_object_or_404(Subscription, id=subscription_id)  
        return obj

@extend_schema(
    description="Получение списка всех подписчиков пользователя.",
    summary="Получение списка всех подписчиков пользователя.",
    tags=["Account"]
)  
class SubscribersListView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Subscription.objects.filter(following=user_id)

@extend_schema(
    description="Получение или удаление подписки на пользователя по id.",
    summary="Получение или удаление подписки на пользователя по id.",
    tags=["Account"]
) 
class SubscribersDetailView(generics.RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        subscription_id = self.kwargs.get('id')
        linker_user = LinkerUser.objects.get(id=user_id)
        self.check_object_permissions(self.request, obj=linker_user)
        obj = get_object_or_404(Subscription, id=subscription_id)  
        return obj