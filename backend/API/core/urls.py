from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views 

# /api/products/
urlpatterns = [
    # Authentication URLs
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # User URLs
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    # Project URLs
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),

    # API Builder URLs
    path('projects/<int:pk>/history', views.ProjectHistoryDetail.as_view(), name='history'),
]