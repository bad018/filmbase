from django.http import HttpResponseRedirect
from django.shortcuts import render
from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from .models import UserWithAccount
from .forms import UserWithAccountForm
from django.contrib import messages


def check_admin(user):
    return user.is_superuser


def userwithaccount_list(request):
    users_with_account = UserWithAccount.objects.all()
    return render(request, 'accounts/templates/list.html', {'users_with_account': users_with_account})


def userwithaccount_detail(request, id):
    user_with_account = get_object_or_404(UserWithAccount, id=id)
    return render(request, 'accounts/templates/detail.html', {'user_with_account': user_with_account})


@user_passes_test(check_admin)
def userwithaccount_create(request):
    if request.method == 'POST':
        form = UserWithAccountForm(request.POST,
                                   request.FILES)
        if form.is_valid():
            user_with_account = form.save()
            messages.success(request, 'Пользователь с аккаунтом добавлен')
            return redirect('users:userwithaccount_detail', id=user_with_account.id)
    else:
        form = UserWithAccountForm()
    return render(request, 'accounts/templates/create.html', {'form': form})


@user_passes_test(check_admin)
def userwithaccount_update(request, id):
    user_with_account = get_object_or_404(UserWithAccount, id=id)
    if request.method == 'POST':
        form = UserWithAccountForm(request.POST, request.FILES, instance=user_with_account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь с аккаунтом изменен')
            return redirect('users:userwithaccount_detail', id=user_with_account.id)
    else:
        form = UserWithAccountForm(instance=user_with_account)
    return render(request, 'accounts/templates/update.html', {'form': form})


@user_passes_test(check_admin)
def userwithaccount_delete(request, id):
    user_with_account = get_object_or_404(UserWithAccount, id=id)
    if request.method == 'POST':
        user_with_account.delete()
        messages.success(request, 'Пользователь с аккаунтом удален')
        return redirect('users:userwithaccount_list')
    return render(request, 'users/userwithaccount/delete.html', {'user_with_account': user_with_account})


class UserWithAccountAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        users = UserWithAccount.objects.all()
        if self.q:
            users = users.filter(user__username__istartswith=self.q)  # Предполагается фильтрация по имени пользователя
        return users
