from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    # Удаление пользователя
    path('user/<int:id>/delete/', views.user_delete, name='user_delete'),
    # Детали пользователя
    path('user/<int:id>/', views.user_detail, name='user_detail'),
    # Список пользователей
    path('user/', views.user_list, name='user_list'),
    # Поиск пользователя
    path('user/search/', views.user_search, name='user_search'),
    # Обновление пользователя
    path('user/<int:id>/update/', views.user_update, name='user_update'),
    # Отправка сообщения
    path('message/<int:id>/send/', views.send_message, name='send_message'),
    # Создание беседы
    path('conversation/create/', views.create_conversation, name='create_conversation'),
    # Список бесед
    path('conversations/', views.conversation_list, name='conversation_list'),
    # Детали беседы
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]
