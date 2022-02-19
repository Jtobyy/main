from django.urls import path
from . import views

app_name = "main"

urlpatterns = [ 
    path('', views.welcome_view, name="welcome"),
    path('index', views.home_view, name="home"),
    path('clothe_sample/<int:clothe_id>', views.clothe_sample_view, name="clothe_sample"),
    path('mail/<int:clothe_id>', views.mail_view, name="sendmail"),
    path('tailorProfile/<int:tailor>', views.tailor_profile_view, name="tailorProfile"),
    path('profile/<int:customer>', views.customer_profile_view, name="profile"),
    path('edit/<str:tailor>/', views.edit_tailor_view, name="edit"),
    path('join', views.join_view, name="join"),
    path('auth', views.auth_view, name="auth"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('measureopt', views.measureopt_view, name="measureopt"),
    path('measuredetails', views.measuredetails_view, name="measuredetails"),
    path('measurehowto', views.measurehowto_view, name="measurehowto"),
    path('promeasure', views.promeasure_view, name="promeasure"),
    path('editprofile', views.edit_customer_view, name="editprofile"),
    path('changepass', views.change_user_pass, name="changepass"),
    path('newaddress', views.newaddress_view, name="newaddress"),
    path('editaddress/<int:address_id>', views.edit_address_view, name="editaddress"),
    path('cart', views.cart_view, name="cart"),
    path('changeaddress/<int:address_id>', views.change_address_view, name="changeaddress"),
    path('logout', views.logout_view, name="logout"),
]