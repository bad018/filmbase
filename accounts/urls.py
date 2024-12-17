from django.urls import path
from . import views

app_name = "userwithaccount"
urlpatterns = [
    path('userwithaccount/', views.userwithaccount_list, name='userwithaccount_list'),
    # Список пользователей
    path('userwithaccount/<int:id>/', views.userwithaccount_detail, name='userwithaccount_detail'),
    # Детали пользователя
    path('userwithaccount/create/', views.userwithaccount_create, name='userwithaccount_create'),
    # Создание пользователя
    path('userwithaccount/<int:id>/update/', views.userwithaccount_update, name='userwithaccount_update'),
    # Обновление пользователя
    path('userwithaccount/<int:id>/delete/', views.userwithaccount_delete, name='userwithaccount_delete'),
]