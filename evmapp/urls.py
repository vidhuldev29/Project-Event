"""evmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [

    path('rg/', views.rg, name='rg'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),

    path('', views.index, name='index'),
    path('admin_index', views.admin_index, name='admin_index'),


    path('about/', views.about, name='about'),
    path('admin_about/', views.admin_about, name='admin_about'),

    path('services/', views.services, name='services'),

    path('booking/',views.booking, name='booking'),
    path('admin_booking/', views.admin_booking, name='admin_booking'),
    path('booking_info/<int:booking_id>/', views.booking_info, name='booking_info'),
    path('admin_booking/delete/<int:booking_id>/', views.admin_delete_booking, name='admin_delete_booking'),

    path('convention', views.conventionview,name='convention'),
    path('convention/<int:id>/gallery/', views.galleryview, name='gallery'),

    path('catering', views.cateringview, name='catering'),
    path('catering/<int:catering_id>/catering_menu/', views.cateringmenuview, name='catering_menu'),

    path('decoration', views.decorationview, name='decoration'),

    path('photography', views.photographyview, name='photography'),
    path('photography/<int:id>/previous_works/', views.worksview, name='previous_works'),

    path('entertainment', views.entertainmentview, name='entertainment'),

    path('accommodation', views.accommodatonview, name='accommodation'),
    path('accommodation/<int:id>/photos_collection/', views.photoview, name='photos_collection'),

    path('transportation', views.transportationview, name='transportation'),



    path('manage_user', views.manage_user, name='manage_user'),
    path('user_info/<str:username>/', views.user_info, name='user_info'),
    path('users/<str:username>/delete/', views.delete_user, name='delete_user'),

    path('manage_convention', views.manage_convention, name='manage_convention'),
    path('convention_info/<int:id>/', views.convention_info, name='convention_info'),
    path('conventions/<int:id>/delete/', views.delete_convention, name='delete_convention'),
    path('add_convention', views.add_convention, name='add_convention'),
    path('add_convention_gallery/', views.add_convention_gallery, name='add_convention_gallery'),
    path('edit_convention/<int:id>/', views.edit_convention, name='edit_convention'),

    path('manage_catering', views.manage_catering, name='manage_catering'),
    path('catering_info/<int:id>/', views.catering_info, name='catering_info'),
    path('caterings/<int:id>/delete/', views.delete_catering, name='delete_catering'),
    path('add_catering', views.add_catering, name='add_catering'),
    path('add_catering_menu/', views.add_catering_menu, name='add_catering_menu'),
    path('edit_catering/<int:id>/', views.edit_catering, name='edit_catering'),

    path('manage_decoration', views.manage_decoration, name='manage_decoration'),
    path('decoration_info/<int:id>/', views.decoration_info, name='decoration_info'),
    path('decorations/<int:id>/delete/', views.delete_decoration, name='delete_decoration'),
    path('add_decoration',views.add_decoration, name='add_decoration'),
    path('edit_decoration/<int:id>/', views.edit_decoration, name='edit_decoration'),

    path('manage_photography', views.manage_photography, name='manage_photography'),
    path('photography_info/<int:id>/', views.photography_info, name='photography_info'),
    path('photographers/<int:id>/delete/', views.delete_photography, name='delete_photography'),
    path('add_photography', views.add_photography, name='add_photography'),
    path('add_photography_works/', views.add_photography_works, name='add_photography_works'),
    path('edit_photography/<int:id>/', views.edit_photography, name='edit_photography'),

    path('manage_entertainment', views.manage_entertainment, name='manage_entertainment'),
    path('entertainment_info/<int:id>/', views.entertainment_info, name='entertainment_info'),
    path('entertainments/<int:id>/delete/', views.delete_entertainment, name='delete_entertainment'),
    path('add_entertainment', views.add_entertainment, name='add_entertainment'),
    path('edit_entertainment/<int:id>/', views.edit_entertainment, name='edit_entertainment'),

    path('manage_accommodation', views.manage_accommodation, name='manage_accommodation'),
    path('accommodation_info/<int:id>/', views.accommodation_info, name='accommodation_info'),
    path('accommodations/<int:id>/delete/', views.delete_accommodation, name='delete_accommodation'),
    path('add_accommodation', views.add_accommodation, name='add_accommodation'),
    path('add_accommodation_photos/', views.add_accommodation_photos, name='add_accommodation_photos'),
    path('edit_accommodation/<int:id>/', views.edit_accommodation, name='edit_accommodation'),

    path('manage_transportation', views.manage_transportation, name='manage_transportation'),
    path('transportation_info/<int:id>/', views.transportation_info, name='transportation_info'),
    path('transportations/<int:id>/delete/', views.delete_transportation, name='delete_transportation'),
    path('add_transportation', views.add_transportation, name='add_transportation'),
    path('edit_transportation/<int:id>/', views.edit_transportation, name='edit_transportation'),



    path('convention_booking',views.convention_booking, name='convention_booking'),
    path('catering_booking', views.catering_booking, name='catering_booking'),
    path('decoration_booking', views.decoration_booking, name='decoration_booking'),
    path('photography_booking', views.photography_booking, name='photography_booking'),
    path('entertainment_booking', views.entertainment_booking, name='entertainment_booking'),
    path('accommodation_booking', views.accommodation_booking, name='accommodation_booking'),
    path('transportation_booking', views.transportation_booking, name='transportation_booking'),

    path('booking/convention/delete/<int:booking_id>/', views.delete_convention_booking, name='delete_convention_booking'),
    path('booking/catering/delete/<int:booking_id>/', views.delete_catering_booking, name='delete_catering_booking'),
    path('booking/decoration/delete/<int:booking_id>/', views.delete_decoration_booking, name='delete_decoration_booking'),
    path('booking/photography/delete/<int:booking_id>/', views.delete_photography_booking, name='delete_photography_booking'),
    path('booking/entertainment/delete/<int:booking_id>/', views.delete_entertainment_booking, name='delete_entertainment_booking'),
    path('booking/accommodation/delete/<int:booking_id>/', views.delete_accommodation_booking, name='delete_accommodation_booking'),
    path('booking/transportation/delete/<int:booking_id>/', views.delete_transportation_booking, name='delete_transportation_booking'),

    path('payment/convention/<int:booking_id>/', views.convention_payment, name='payment_convention'),
    path('payment/catering/<int:booking_id>/', views.catering_payment, name='payment_catering'),
    path('payment/decoration/<int:booking_id>/', views.decoration_payment, name='payment_decoration'),
    path('payment/photography/<int:booking_id>/', views.photography_payment, name='payment_photography'),
    path('payment/entertainment/<int:booking_id>/', views.entertainment_payment, name='payment_entertainment'),
    path('payment/accommodation/<int:booking_id>/', views.accommodation_payment, name='payment_accommodation'),
    path('payment/transportation/<int:booking_id>/', views.transportation_payment, name='payment_transportation'),

]


