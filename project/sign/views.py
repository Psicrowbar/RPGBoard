from email.headerregistry import Group

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rpg.models import Categories


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Categories.objects.get(id=pk)
    category.subscribers.add(user)
    message = ('вы подписались на категорию: ')
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Categories.objects.get(id=pk)
    category.subscribers.remove(user)
    message = ('вы отписались от категории: ')
    return render(request, 'subscribe.html', {'category': category, 'message': message})


