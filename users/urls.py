from django.urls import path

from users.views.roles import *
from users.views.usuarios import *
from users.views.usuarios_dpto import *

urlpatterns = [

    # USUARIOS
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('lista-usuarios/', UserListView.as_view(), name='usuarios_list'),
    path('crear-usuario', UserCreateView.as_view(), name='usuarios_create'),
    path('actualizar-usuario/<int:pk>/', UserUpdateView.as_view(), name='usuarios_update'),
    path('usuarios/<int:pk>/', UserDetailView.as_view(), name='usuarios_detail'),
    path('usuarios/<int:pk>/reset-password/', UserResetPasswordView.as_view(), name='usuarios_reset_password'),
    path('usuarios/cambiar-password/', UserChangePasswordView.as_view(), name='usuarios_change_password'),
    path('perfil/', UserProfileUpdateView.as_view(), name='perfil'),

    # ROLES

    path('roles/', RoleListView.as_view(), name='roles_list'),
    path('roles/crear/', RoleCreateView.as_view(), name='roles_create'),
    path('roles/<int:pk>/editar/', RoleUpdateView.as_view(), name='roles_update'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='roles_detail'),

    # DPTO
    path('lista-usuarios_dpto/', UserDptoListView.as_view(), name='usuarios_dpto_list'),
    path('crear-usuario-dpto', UserDptoCreateView.as_view(), name='usuarios_dpto_create'),
    path('actualizar-usuario-dpto/<int:pk>/', UserDptoUpdateView.as_view(), name='usuarios_dpto_update'),
    path('usuarios-dpto/<int:pk>/', UserDptoDetailView.as_view(), name='usuarios_dpto_detail'),
    # path('usuarios_dpto/<int:pk>/reset-password/', UserDptoResetPasswordView.as_view(),
    #      name='usuarios_dpto_reset_password'),
    path('usuarios_dpto/cambiar-password/', UserDptoChangePasswordView.as_view(), name='usuarios_dpto_change_password'),
]
