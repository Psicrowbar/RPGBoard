from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Reply, Categories, Author, BaseRegisterForm
from django.contrib.auth.models import User, Group
from .forms import PostForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'rpg.post_create'
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # success_url = reverse_lazy('your_success_url')

    def form_valid(self, form):
        # kek
        kek = form.save(commit=False)
        user = self.request.user
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            author = Author.objects.create(user=user)
        post = form.save(commit=False)
        post.author = author
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = 'rpg.post_create'
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'rpg.post_delete'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ReplyCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'rpg.comm_create'
    form_class = ReplyForm
    model = Reply
    template_name = 'comm_create.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        if self.request.method == 'POST':
            pk = self.request.path.split('/')[-3]
            sender = self.request.user
            reply.post = Post.objects.get(id=pk)
            reply.sender = User.objects.get(username=sender)
        reply.save()
        return super().form_valid(form)

    def get_success_url(self):
        url = '/'.join(self.request.path.split('/')[0:-2])
        return url


class Replies(PermissionRequiredMixin, ListView):
    permission_required = 'rpg.comm_post'
    model = Reply
    template_name = 'comm_post.html'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post__author_id=self.request.user.id)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


'''class CategoryList(ListView):
    model = Categories
    template_name = 'categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Categories, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.categories).order_by('-time_created')
        return queryset
'''
