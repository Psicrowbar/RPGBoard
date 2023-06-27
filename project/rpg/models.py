from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from django import forms


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


tank = 'TN'
healer = 'HL'
damager = 'DD'
guild_master = 'GM'
quest_giver = 'KG'
smith = 'KZ'
tanner = 'KV'
potion_maker = 'ZV'
spell_master = 'MZ'

CATEGORIES = [
    (tank, 'Танк'),
    (healer, 'Хил'),
    (damager, 'ДД'),
    (guild_master, 'Гилдмастер'),
    (quest_giver, 'Квестгивер'),
    (smith, 'Кузнец'),
    (tanner, 'Кожевник'),
    (potion_maker, 'Зельевар'),
    (spell_master, 'Мастер заклинаний'),
]


class Categories(models.Model):
    name = models.CharField(max_length=17, choices=CATEGORIES, default=tank)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Название")
    text = RichTextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    video_count = models.PositiveIntegerField(default=0)
    image_count = models.PositiveIntegerField(default=0)
    max_video_count = 1
    max_image_count = 3

    def add_video(self):
        if self.video_count >= self.max_video_count:
            raise ValueError("Превышено максимальное количество видео")
        self.video_count += 1

    def add_image(self):
        if self.image_count >= self.max_image_count:
            raise ValueError("Превышено максимальное количество изображений")
        self.image_count += 1

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_list', args=[str(self.id)])


class Reply(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)


class News(models.Model):
    title = models.CharField(max_length=100, default="Default value")
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


