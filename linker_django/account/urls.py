from .views import *
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='accounts_list_create'),
    path('accounts/<int:id>/', AccountRetrieveUpdateDestroyView.as_view(), name='accounts_detail'),
    path('accounts/<int:user_id>/photos/', AccountPhotoListCreateView.as_view(), name='accounts_photos_list_create'),
    path('accounts/<int:user_id>/photos/<int:photo_id>/', AccountPhotoRetrieveDestroyView.as_view(), name='accounts_photos_detail'),
    path('accounts/<int:user_id>/subscriptions/', SubscriptionListCreateView.as_view(), name='accounts_subscription'),
    path('accounts/<int:user_id>/subscriptions/<int:id>/', SubscriptionDetailView.as_view(), name='accounts_subscription_detail'),
    path('accounts/<int:user_id>/subscribers/', SubscribersListView.as_view(), name='accounts_subscribers'),
    path('accounts/<int:user_id>/subscribers/<int:id>/', SubscribersDetailView.as_view(), name='accounts_subscribers_dateil'),
    path('accounts/signin/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('accounts/signin/token/refresh/', RefreshLoginView.as_view(), name='token_refresh'),
    path('accounts/logout/', LogoutView.as_view(), name='logout_view'),
]