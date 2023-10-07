from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('<int:user_id>/get_posts/', views.get_posts, name='get_posts'),
    path('<int:user_id>/create_post/', views.create_post, name='create_post'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('', views.userpage),
    path("<int:user_id>/", views.userpage, name="userpage"),

    path("handle_friend_request/<int:user_id>/", views.handle_friend_request, name='handle_friend_request'),
    path("accept_friend_request/<int:notification_id>/", views.accept_friend_request, name='accept_friend_request'),
    path('notifications/', views.notifications, name='notifications'),
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('<int:user_id>/friends/', views.user_friends, name='user_friends'),

# URL pattern for user registration
    path('signup/', views.register, name='signup'),

    # URL pattern for user login
    path('login/', CustomLoginView.as_view(), name='login'),

    # URL pattern for user logout (if applicable)
    #path('logout/', views.logout_view, name='logout'),

]