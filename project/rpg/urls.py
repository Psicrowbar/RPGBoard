from allauth.account.views import LoginView, LogoutView
from django.urls import path

from sign import views
from .views import PostsList, PostDetail, PostCreate, PostDelete, ReplyCreate, Replies, BaseRegisterView
#from .views import upgrade_me

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   #path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/reply/', ReplyCreate.as_view(), name='comm_post'),

   path('my_replies/', Replies.as_view(), name='comm_post'),
   path('login/',
         LoginView.as_view(template_name='account/login.html'),
         name='login'),
   path('logout/',
         LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
   path('signup/',
         BaseRegisterView.as_view(template_name='account/signup.html'),
         name='signup'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.unsubscribe, name='subscribe_success'),
]
   #path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
