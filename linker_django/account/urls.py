from .views import *
from django.urls import path

urlpatterns = [
    path('account/', AccountListCreateView.as_view(), name='account_list_create'),
    path('account/<int:id>/', AccountRetrieveUpdateDestroyView.as_view(), name='account_detail'),
    path('account/<int:user_id>/photo/', AccountPhotoListCreateView.as_view(), name='account_photo_list_create'),
    path('account/<int:user_id>/photo/<int:photo_id>/', AccountPhotoRetrieveDestroyView.as_view(), name='account_photo_detail'),
    path('account/<int:user_id>/subscription/', SubscriptionListCreateView.as_view(), name='account_subscription'),
    path('account/<int:user_id>/subscription/<int:id>/', SubscriptionDetailView.as_view(), name='account_subscription_detail'),
]