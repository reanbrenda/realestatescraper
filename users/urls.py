from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-create'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check/', views.check_auth, name='check-auth'),
    path('check-admin/', views.check_admin, name='check-admin'),
    path('admin/users/', views.UserListView.as_view(), name='user-list'),
    path('admin/user/', views.add_user, name='add-user'),
    path('admin/user/<int:user_id_to_delete>/', views.delete_user, name='delete-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
