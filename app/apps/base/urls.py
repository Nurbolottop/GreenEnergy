from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/verify/', views.verify_human_view, name='verify_human'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('set-language-ajax/', views.set_language_ajax, name='set_language_ajax'),
]
