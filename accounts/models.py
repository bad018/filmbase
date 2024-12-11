from django.db import models
from django.conf import settings
from django.contrib.auth.forms import User
from django.core.validators import MaxValueValidator
from films.models import MyModel
from django import forms
import datetime

class UserWithAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    birthday = models.DateField("Дата рождения", blank=True, null=True,
                                validators=[
                                    MaxValueValidator(
                                        limit_value=datetime.date.today)
                                ])
    avatar = models.ImageField(
        "Фото", upload_to='photos/', blank=True, null=True)
    address = models.TextField("Адрес", blank=True, null=True)
    bio = models.TextField("Биография", blank=True, null=True)

    def age(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        return today.year - self.birthday.year \
            - ((today.month, today.day) < (self.birthday.month,
                                           self.birthday.day))

    class Meta:
        ordering = ["user"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name

class Conversation(MyModel):
    participants = models.ManyToManyField(
        UserWithAccount,
        verbose_name="Участники",
        related_name="conversations"
    )
    subject = models.CharField("Тема", max_length=255)

    def __str__(self):
        return self.subject

class Message(MyModel):
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        verbose_name="Разговор", 
        related_name="messages"
    )
    sender = models.ForeignKey(
        UserWithAccount, 
        on_delete=models.CASCADE, 
        verbose_name="Пользователь, отправивший сообщение", 
        related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        UserWithAccount, 
        on_delete=models.CASCADE, 
        verbose_name="Пользователь, получивший сообщение", 
        related_name="received_messages"
    )
    content = models.TextField("Сообщение")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f'From {self.sender} to {self.recipient}: {self.content[:20]}'