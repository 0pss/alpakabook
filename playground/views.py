from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import User_dev
# Create your views here.
# request --> response

def userpage(request, user_id):
    print(user_id)
    try:
        user = User_dev.objects.get(pk=user_id)
    except User_dev.DoesNotExist:
        raise Http404("User does not exist")
    print(user)
    return render(request, "hello.html",{'user':user})