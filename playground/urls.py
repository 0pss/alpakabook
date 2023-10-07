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

# URL pattern for user registration
    path('signup/', views.register, name='signup'),

    # URL pattern for user login
    path('login/', CustomLoginView.as_view(), name='login'),

    # URL pattern for user logout (if applicable)
    #path('logout/', views.logout_view, name='logout'),

]