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
        viewed_user = User_dev.objects.get(id=user_id)
    except User_dev.DoesNotExist:
        raise Http404("User does not exist")

    # Determine the friendship status
    friendship = Friendship.objects.filter(
        (Q(sender=request.user, receiver=viewed_user) | Q(sender=viewed_user, receiver=request.user))).first()

    if friendship is not None:
        # Users are friends
        viewed_user.friendship_status = friendship.status
    else:
        viewed_user.friendship_status = 'send_request'

    viewed_user.friendship_status_display = dict(Friendship.STATUS_CHOICES)[viewed_user.friendship_status]
    is_friends = get_friendship_status(request.user, viewed_user)

    return render(request, 'hello.html', {'user': viewed_user, 'is_friends': is_friends})


def userpage_json(request, user_id):
    print(user_id)
    try:
        viewed_user = User_dev.objects.get(id=user_id)
    except User_dev.DoesNotExist:
        raise Http404("User does not exist")

    result = {
        "username": viewed_user.username,
        "FavIce": viewed_user.FavIce,
        "Shoesize": viewed_user.Shoesize,
        "Age": viewed_user.Age,
        "Hobbies": viewed_user.Hobbies,
    }

    return JsonResponse(result)


from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
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
    try:
        viewed_user = User_dev.objects.get(id=user_id)
    except User_dev.DoesNotExist:
        raise Http404("User does not exist")

    is_friends = get_friendship_status(request.user, viewed_user)
    posts = Post.objects.filter(user_id=user_id).order_by('-timestamp')
    return render(request, 'post_list.html', {'posts': posts,'is_friends': is_friends})


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        print("FILES: ", request.FILES)
        if form.is_valid():
            user = form.save()
            # Redirect to a success page or login the user
            return redirect('login')
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
    print("notification_id: ", notification_id, notification.receiver, request.user, notification.notification_type)
    if notification.receiver == request.user and notification.notification_type == 'friend_request':
        # Update the friendship status
        print("Friend status will be updated")
        try:
            friendship = Friendship.objects.get(sender=notification.sender, receiver=notification.receiver)
            friendship.status = 'friends'
            friendship.save()

            # Create a Notification for the sender
            notification2 = Notification(sender=notification.receiver, receiver=notification.sender,
                                         notification_type='friend_request_accepted', is_read=False)
            notification2.save()
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


def mark_notification_read(request, notification_id):
    print("marking as read ", notification_id)
    try:
        notification = Notification.objects.get(id=notification_id, receiver=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False})


def get_friendship_status(viewing_user, profile_user):
    if viewing_user == profile_user:
        return True

    try:
        friendship = Friendship.objects.get(
            Q(sender=viewing_user, receiver=profile_user, status='friends') |
            Q(sender=profile_user, receiver=viewing_user, status='friends')
        )
        return True  # They are friends
    except Friendship.DoesNotExist:
        return False  # They are not friends


from django.shortcuts import get_object_or_404


def user_friends(request, user_id):
    # Get the user with the specified user_id
    user = get_object_or_404(User_dev, id=user_id)

    # Query the Friendship model to get the user's friends
    sender_friends = Friendship.objects.filter(sender=user, status='friends').values_list('receiver__id', flat=True)
    receiver_friends = Friendship.objects.filter(receiver=user, status='friends').values_list('sender__id', flat=True)

    # Combine the friend IDs from both sender and receiver sides
    friend_ids = list(sender_friends) + list(receiver_friends)

    return JsonResponse({'friends': friend_ids})


def search_results(request):
    search_query = request.GET.get('search_query')
    if search_query:
        # Perform a case-insensitive search for usernames
        results = User_dev2.objects.filter(username__icontains=search_query)
    else:
        results = None

    return render(request, 'search_results.html', {'results': results, 'search_query': search_query})


def friend_list(request, user_id):
    user = get_object_or_404(User_dev, id=user_id)

    # Get friends where status is 'friends'
    friends = Friendship.objects.filter(
        Q(sender=user, status='friends') | Q(receiver=user, status='friends')
    )

    print(friends)

    return render(request, 'friend_list.html', {'friends': friends, 'viewed_user_id': user_id})


def page_not_found(request, exeption):
    """
    Page not found Error 404
    """

    return render(request, '404.html', status=404)


def upload_profile_picture(request, user_id):
    if request.method == 'POST':
        profile_picture = request.FILES['profile_picture']
        print(user_id)
        user_profile = get_object_or_404(User_dev, id=user_id)
        user_profile.profile_picture = profile_picture
        user_profile.save()
        is_friends = get_friendship_status(user_profile, user_profile)

        return redirect(f'/user/{user_id}/')


def splash_screen(request):
    return render(request, 'splash.html')  # Create a "splash.html" template for your splash screen


def user_edit(request, user_id):
    print(request)
    if request.method == 'POST':
        print(request)
        # Retrieve and process the form data
        age = request.POST['Age']
        fav_ice = request.POST['FavIce']
        shoesize = request.POST['Shoesize']
        hobbies = request.POST['Hobbies']

        # Update the user's data in the database
        user = User_dev2.objects.get(pk=user_id)
        user.Age = age
        user.FavIce = fav_ice
        user.Shoesize = shoesize
        user.Hobbies = hobbies
        user.save()

        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
