from django.db import models
from django.contrib.auth.forms import User
from django.core.validators import MinValueValidator, MaxValueValidator
from films.models import MyModel
import datetime

class UserWithAccount(User, MyModel):
    name = models.CharField("Имя", max_length=400)
    birthday = models.DateField("Дата рождения", blank=True, null=True,
                                validators=[
                                    MaxValueValidator(
                                        limit_value=datetime.date.today)
                                ])
    avatar = models.ImageField(
        "Фото", upload_to='photos/', blank=True, null=True)
    mail = models.EmailField("Почта", max_length=100)
    address = models.TextField("Адрес", blank=True, null=True)
    language_preference = models.CharField("Предпочтительный язык", max_length=100,
                                            default='Русский')
    bio = models.TextField("Биография", blank=True, null=True)
    pronouns = models.CharField("Местоимения", max_length=10, null=True)
    social_url = models.URLField("Социальные сети", blank=True, null=True)

    def age(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        return today.year - self.birthday.year \
            - ((today.month, today.day) < (self.birthday.month,
                                           self.birthday.day))

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name
    

class Message(MyModel):
    author = models.ForeignKey(
        UserWithAccount, on_delete=models.CASCADE, verbose_name="Автор")