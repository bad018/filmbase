from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from .models import UserWithAccount, Message, Conversation
from .forms import UserWithAccountForm, MessageForm, ConversationForm
from django.contrib import messages
from django.db.models import Count

User = get_user_model()


def check_admin(user):
    return user.is_superuser


def user_delete(request, id):
    user_with_account = get_object_or_404(UserWithAccount, user_id=id)

    if request.method == 'POST':
        user_with_account.delete()
        messages.success(request, 'Аккаунт успешно удален.')
        return redirect('signup:signup')

    return render(request, 'accounts/user/delete.html', {'user_with_account': user_with_account,
                                                         'user': request.user})


def user_detail(request, id):
    user_with_account = get_object_or_404(UserWithAccount, user_id=id)
    return render(request, 'accounts/user/detail.html', {'user_with_account': user_with_account})


def user_list(request):
    query = request.GET.get('query')
    users_with_account = UserWithAccount.objects.exclude(user=request.user)  # Исключаем текущего пользователя
    if query:
        users_with_account = users_with_account.filter(user__username__icontains=query)

    return render(request, 'accounts/user/list.html', {'users_with_account': users_with_account})


def user_search(request):
    query = request.GET.get('q')
    users_with_account = UserWithAccount.objects.all()

    if query:
        users_with_account = users_with_account.filter(
            user__username__icontains=query)

    return render(request, 'accounts/user/list.html', {'users_with_account': users_with_account})


def user_update(request, id):
    user_with_account = get_object_or_404(UserWithAccount, user_id=id)

    if request.method == 'POST':
        form = UserWithAccountForm(request.POST, request.FILES, instance=user_with_account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно обновлен')
            return redirect('accounts:user_detail', id=user_with_account.user.id)
    else:
        form = UserWithAccountForm(instance=user_with_account)

    return render(request, 'accounts/user/update.html', {'form': form})


def send_message(request, id):
    recipient = get_object_or_404(User, id=id)  # Получатель
    sender = request.user  # Отправитель — текущий пользователь

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Ищем беседу с двумя участниками: отправителем и получателем
            conversation = Conversation.objects.annotate(num_participants=Count('participants')).filter(
                participants=sender
            ).filter(
                participants=recipient
            ).filter(
                num_participants=2  # Только беседы с двумя участниками
            ).first()

            # Если беседы нет, создаем новую
            if not conversation:
                conversation = Conversation.objects.create(
                    subject=f"Беседа между {sender.username} и {recipient.username}"
                )
                conversation.participants.add(sender, recipient)  # Добавляем участников

            # Создаем сообщение
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.conversation = conversation  # Связываем сообщение с беседой
            message.save()

            return redirect('accounts:conversation_detail', conversation_id=conversation.id)  # Перенаправляем в чат
    else:
        form = MessageForm()

    return render(request, 'accounts/message/send.html', {
        'form': form,
        'recipient': recipient
    })


def create_conversation(request):
    if request.method == 'POST':
        form = ConversationForm(request.POST, user=request.user)  # Передаем текущего пользователя в форму
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.save()  # Сохраняем беседу
            form.save_m2m()  # Сохраняем участников

            # Добавляем текущего пользователя в беседу
            conversation.participants.add(request.user)

            messages.success(request, 'Беседа успешно создана')
            return redirect('accounts:conversation_list')  # Перенаправляем на список бесед
    else:
        form = ConversationForm(user=request.user)  # Передаем текущего пользователя в форму

    return render(request, 'accounts/conversation/create.html', {'form': form})


def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'accounts/conversation/list.html', {'conversations': conversations})


def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages_list = conversation.messages.all().order_by('created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation

            # Определяем получателя (все участники, кроме отправителя)
            participants = conversation.participants.exclude(id=request.user.id)
            if participants.exists():
                message.recipient = participants.first()  # Отправляем первому участнику
            else:
                messages.error(request, 'Невозможно отправить сообщение: нет получателя.')
                return redirect('accounts:conversation_detail', conversation_id=conversation.id)

            message.save()
            return redirect('accounts:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    return render(request, 'accounts/conversation/detail.html', {
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
    })
