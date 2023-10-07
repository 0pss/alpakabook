from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import User_dev2 as User_dev


# Create your views here.
# request --> response

def userpage(request, user_id):
    print(user_id)
    try:
        user = User_dev.objects.get(pk=user_id)
    except User_dev.DoesNotExist:
        raise Http404("User does not exist")
    print(user)
    return render(request, "hello.html", {'user': user})


from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
from .forms import PostForm


def create_post(request, user_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            try:
                user_instance = User_dev.objects.get(pk=user_id)
                post.user = user_instance  # Assuming you have user authentication in place
                post.save()
            except User_dev.DoesNotExist:
                # Handle the case where the user with the specified ID doesn't exist
                pass

            return JsonResponse({'message': 'Post created successfully'})

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
