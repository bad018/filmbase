from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from films.models import MyModel
import datetime


class UserWithAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
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
        verbose_name = "Зарегистрировавшийся пользователь"
        verbose_name_plural = "Зарегистрировавшиеся пользователи"

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="Отправитель"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name="Получатель"
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Беседа",
        default=1
    )
    content = models.TextField("Текст сообщения")
    attachment = models.FileField("Прикрепленный файл", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение от {self.sender.username} к {self.recipient.username}"


class Conversation(MyModel):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # Участники беседы
        verbose_name="Участники",
        blank=True
    )
    subject = models.CharField("Тема", max_length=255)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"

    def __str__(self):
        return self.subject