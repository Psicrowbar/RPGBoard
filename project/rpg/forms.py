from django import forms
from django.forms import ModelForm, BooleanField
from .models import Post, Reply, Categories
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(ModelForm):
    check_box = BooleanField(label='confirm')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'author', 'check_box']
        # не забываем включить галочку в поля, иначе она не будет показываться на странице!


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['text']


class SubscriptionForm(forms.Form):
    email = forms.EmailField()
    category = forms.ModelChoiceField(queryset=Categories.objects.all())
