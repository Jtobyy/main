from django.urls import path
from . import views

app_name = "main"

urlpatterns = [ 
    path('', views.welcome_view, name="welcome"),
    path('index', views.home_view, name="home"),
    path('clothe_sample/<int:clothe_id>', views.clothe_sample_view, name="clothe_sample"),
    path('mail/<int:clothe_id>', views.mail_view, name="sendmail"),
    path('tailorProfile/<int:tailor>/', views.tailor_profile_view, name="tailorProfile"),
    path('edit/<str:tailor>/', views.edit_view, name="edit"),
    path('join', views.join_view, name="join"),
    path('auth', views.auth_view, name="auth"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
]