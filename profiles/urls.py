from django.urls import path,include
from .views import ProfilesApi,ProfilesUpdateApi
from rest_framework.authtoken import views

app_name = 'profile'
urlpatterns = [
    path('profile/<str:username>',ProfilesApi.as_view(),name="profile-detail"),
    path('profile/<str:username>/update',ProfilesUpdateApi.as_view(),name="profile-update"),
    path('token-auth/', views.obtain_auth_token),
]