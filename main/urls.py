from django.urls import path
from . import views

app_name = "main"

urlpatterns = [ 
    path('', views.welcome_view, name="welcome"),
    path('shop', views.shop_view, name="shop"),
    path('shopfilter/', views.shop_filter_view, name="shopfilter"),
    path('exshopfilter/<str:filter>', views.ex_shop_filter_view, name="exshopfilter"),
    path('fabrics', views.fabrics_view, name="fabrics"),
    path('fabricsfilter/', views.fabrics_filter_view, name="fabricsfilter"),
    path('exfabricsfilter/<str:filter>', views.ex_fabrics_filter_view, name="exfabricsfilter"),
    path('tailors', views.tailors_list_view, name="tailors_list"),
    path('clothe_sample/<int:clothe_id>', views.clothe_sample_view, name="clothe_sample"),
    path('fabric_sample/<int:fabric_id>', views.fabric_sample_view, name="fabric_sample"),
    path('mail/<int:clothe_id>', views.mail_view, name="sendmail"),
    path('profile/<str:user>', views.external_profile_view, name="profile"),
    path('tailorProfile/<int:tailor_id>', views.tailor_profile_view, name="tailorProfile"),
    path('custProfile/<int:customer_id>', views.customer_profile_view, name="custProfile"),
    path('sellerProfile/<int:seller_id>', views.seller_profile_view, name="sellerProfile"),
    path('editTailorProfile/<int:tailor_id>/', views.edit_tailor_view, name="editTailorProfile"),
    path('editCustProfile<int:customer_id>', views.edit_customer_view, name="editCustProfile"),
    path('editSellerProfile<int:seller_id>', views.edit_seller_view, name="editSellerProfile"),

    path('tailorRegInfo', views.tailor_reg_info_view, name="tailorRegInfo"),
    path('sellerRegInfo', views.seller_reg_info_view, name="sellerRegInfo"),
    path('tailorReg', views.tailor_reg_view, name="tailorReg"),
    path('sellerReg', views.seller_reg_view, name="sellerReg"),

    path('partner', views.partner_view, name="partner"),
    path('popauth', views.popauth_view, name="popauth"),
    path('auth', views.auth_view, name="auth"),
    path('login', views.login_view, name="login"),
    path('login2', views.poplogin_view, name="login2"),
    path('register', views.register_view, name="register"),
    path('register2', views.poplogin_view, name="register2"),
    path('measureopt', views.measureopt_view, name="measureopt"),
    path('measuredetails', views.measuredetails_view, name="measuredetails"),
    path('measurehowto', views.measurehowto_view, name="measurehowto"),
    path('promeasure', views.promeasure_view, name="promeasure"),
    path('changepass', views.change_user_pass, name="changepass"),
    path('newaddress', views.newaddress_view, name="newaddress"),
    path('editaddress/<int:address_id>', views.edit_address_view, name="editaddress"),
    path('cart', views.cart_view, name="cart"),
    path('changeaddress/<int:address_id>', views.change_address_view, name="changeaddress"),
    path('logout', views.logout_view, name="logout"),

    path('profile/<str:user>', views.external_profile_view, 'profile', **('name',),)
    path('partnerProfile/<int:partner_id>', views.partner_profile_view, 'partnerProfile', **('name',)),
    path('partner_reg', views.partner_reg_view, 'partner_reg', **('name',)),
    path('partner', views.partner_view, 'partner', **('name',)),
    path('request_submitted', views.success_reg_view, 'request_submitted', **('name',)),
    path('add_partner/<int:partner_id>', views.add_partner_view, 'add_partner', **('name',)),  
]