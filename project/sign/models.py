from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.db import models
from rpg.models import Categories, Post


class NewPost(Post):
    new_ppst = Post

    def notify_subscribers(self):
        # Получаем все подписки на данную категорию
        subscriptions = Subscription.objects.filter(category=self.category)

        # Составляем список получателей
        recipients = [subscription.email for subscription in subscriptions]

        # Формируем тему и текст сообщения
        subject = f"Новый пост в категории {self.category.name}"
        message = render_to_string('email/new_post_notification.html', {'post': self})

        # Отправляем сообщение
        send_mail(subject, message, 'noreply@example.com', recipients)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.notify_subscribers()


class Subscription(Categories):  # модель хранения подптсаных категорий
    email = models.EmailField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='favorite_category')


#Categories, on_delete=models.CASCADE, related_name='favorite_category')