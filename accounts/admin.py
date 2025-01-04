from django.contrib import admin
from .models import UserWithAccount, Message, Conversation

admin.site.register(UserWithAccount)
admin.site.register(Message)
admin.site.register(Conversation)
