from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.http import Http404

from .models import User_dev2 as User_dev

from django.db.models import Q


# Create your views here.
# request --> response

def userpage(request, user_id):
    print(user_id)
    try:
        user = User_dev.objects.get(pk=user_id)
    except User_dev.DoesNotExist:
        raise Http404("User does not exist")
    # print(user)
    # return render(request, "hello.html", {'user': user})

    viewed_user = User_dev.objects.get(id=user_id)
    logged_in_user = request.user

    # Determine the friendship status

    friendship = Friendship.objects.filter(
        (Q(sender=logged_in_user, receiver=viewed_user) | Q(sender=viewed_user, receiver=logged_in_user))).first()

    if friendship is not None:
        # Users are friends
        viewed_user.friendship_status = friendship.status
    else:
        viewed_user.friendship_status = 'send_request'

    viewed_user.friendship_status_display = dict(Friendship.STATUS_CHOICES)[viewed_user.friendship_status]

    print("When requesting user, this status was determined: ", viewed_user.friendship_status)
    return render(request, 'hello.html', {'user': viewed_user})


from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User_dev2, Post  # Import your User_dev and Post models
from .forms import PostForm  # Import your PostForm if you have one


@login_required
def create_post(request, user_id):
    if request.user.id != user_id:
        # Check if the logged-in user's ID matches the user_id in the URL
        return HttpResponseForbidden("You can only create posts on your own page.")

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                user_instance = User_dev.objects.get(pk=user_id)
                post.user = user_instance  # Associate the post with the user's profile
                post.save()
                return JsonResponse({'message': 'Post created successfully'})
            except User_dev.DoesNotExist:
                # Handle the case where the user with the specified ID doesn't exist
                pass

    return JsonResponse({'message': 'Invalid form data'})


def get_posts(request, user_id):
    posts = Post.objects.filter(user_id=user_id).order_by('-timestamp')
    return render(request, 'post_list.html', {'posts': posts})


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("HERE")
            user = form.save()
            # Redirect to a success page or login the user
            # return redirect('login')
        else:
            errors = form.errors
            print(errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth.views import LoginView, LogoutView


# Login view
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Call the parent class's form_valid method to log the user in
        response = super().form_valid(form)

        # Redirect to the user's profile page
        user_id = self.request.user.id
        return redirect('userpage', user_id=user_id)


# Logout view
class CustomLogoutView(LogoutView):
    next_page = 'login'


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user_profile(request):
    # Your profile view logic here
    return render(request, 'hello.html')  # Use the appropriate template


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Friendship

# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def handle_friend_request(request, user_id):
    if request.method == 'POST':
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        print(post_data)
        status = post_data['status']
        receiver = User_dev.objects.get(id=user_id)
        sender = request.user

        print(status)

        # Handle the friend request based on the status
        if status == 'send_request':
            # Create a new friendship request
            friendship = Friendship(sender=sender, receiver=receiver, status='request_sent')
            friendship.save()
            # Create a Notification for the recipient
            notification = Notification(sender=sender, receiver=receiver, notification_type='friend_request')
            notification.save()

            new_status = 'request_sent'
        elif status == 'request_sent':
            # Accept the friend request
            friendship = Friendship.objects.get(sender=receiver, receiver=sender)
            friendship.status = 'friends'
            friendship.save()
            new_status = 'friends'
        else:
            # Handle other cases as needed
            new_status = status

        print("nwéw Status: ", new_status, "   ", dict(Friendship.STATUS_CHOICES))
        return JsonResponse({'success': True, 'new_status': new_status,
                             'new_status_display': dict(Friendship.STATUS_CHOICES)[new_status]})
    return JsonResponse({'success': False})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Friendship, Notification


@login_required
def accept_friend_request(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    print("notification_id: ",  notification_id, notification.receiver,  request.user, notification.notification_type)
    if notification.receiver == request.user and notification.notification_type == 'friend_request':
        # Update the friendship status
        print("Friend status will be updated")
        try:
            friendship = Friendship.objects.get(sender=notification.sender, receiver=notification.receiver)
            friendship.status = 'friends'
            friendship.save()

            # Create a Notification for the sender
            notification = Notification(sender=notification.receiver, receiver=notification.sender,
                                        notification_type='friend_request_accepted')
            notification.save()
        except Friendship.DoesNotExist:
            # Handle the case where the friendship doesn't exist
            pass

        # Mark the notification as read
        notification.is_read = True
        notification.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


from .models import Notification


def notifications(request):
    # Retrieve and pass unread notifications to the template
    unread_notifications = Notification.objects.filter(receiver=request.user, is_read=False)

    return render(request, 'notifications.html', {'unread_notifications': unread_notifications})