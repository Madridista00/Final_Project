from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.TeamsList.as_view(), name='main'),
    path('team/<int:pk>/', views.TeamsDetail.as_view(), name='team'),
    path('team_create/', views.TeamCreate.as_view(), name='team_create'),
    path('team_update/<int:pk>/', views.TeamUpdate.as_view(), name='team_update'),
    path('team_delete/<int:pk>/', views.TeamDelete.as_view(), name='team_delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),

]
