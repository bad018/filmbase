from django import forms
from django.contrib.auth import get_user_model
from .models import UserWithAccount, Message, Conversation

User = get_user_model()


class UserWithAccountForm(forms.ModelForm):
    class Meta:
        model = UserWithAccount
        fields = ['birthday', 'avatar', 'address', 'bio']
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'},
                                        format="%Y-%m-%d")
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'attachment']


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['subject', 'participants']
        widgets = {
            'participants': forms.CheckboxSelectMultiple,  # Выбор участников
        }

    def __init__(self, *args, **kwargs):
        # Получаем текущего пользователя из kwargs и удаляем его, чтобы он не попал в форму
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Фильтруем участников, исключая текущего пользователя
        if self.user:
            self.fields['participants'].queryset = User.objects.exclude(id=self.user.id)
