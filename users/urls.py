from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users import views
from users.services import email_verification, block_user

app_name = 'users'

urlpatterns = [path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
               path('logout/', LogoutView.as_view(next_page='mailing:home'), name='logout'),
               path('register/', views.UserRegisterView.as_view(), name='register'),
               path("users/", views.UserListView.as_view(), name="users"),
               path("detail/<int:pk>/", views.UserDetailView.as_view(), name="detail"),
               path("update/<int:pk>/", views.UserUpdateView.as_view(), name="update"),
               path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
               path("email-confirmation/", views.EmailConfirmationView.as_view(), name="email_confirmation"),
               path("password-recovery/", views.PasswordRecoveryView.as_view(), name="password_recovery"),
               path("password-confirmation/", views.PasswordConfirmationView.as_view(), name="password-confirmation"),
               path("block_user/<int:pk>", block_user, name="block_user"),
            ]
