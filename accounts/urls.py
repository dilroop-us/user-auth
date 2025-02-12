from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/<int:pk>/', views.update_user, name='update_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    
]
