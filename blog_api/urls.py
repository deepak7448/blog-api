from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls import url,re_path
#from allauth.account.views import LoginView
from dj_rest_auth.registration.views import RegisterView,VerifyEmailView,ConfirmEmailView
from dj_rest_auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetConfirmView,PasswordChangeView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('post.urls',namespace='posts')),
    path('',include('profiles.urls',namespace='profile')),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', LoginView.as_view(),name='account_signin'),
    path('logout/', LogoutView.as_view(),name='account_login'),
    path('signup/',RegisterView.as_view(),name='account_signup'),
    path('verify-email/',VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account/confirm-email/',VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account/confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
    path('account/confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('account/password/change/', PasswordChangeView.as_view(),name='account_change_password'),
    path('account/password-reset/', PasswordResetView.as_view(),name='password_reset'),
    path('account/password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('accounts/', include('dj_rest_auth.urls')),
    #path('accounts/registration/', include('dj_rest_auth.registration.urls'))

    #path('accounts/', include('allauth.urls')),  
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
