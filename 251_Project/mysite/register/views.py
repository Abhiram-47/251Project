from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from .forms import newuser


# Create your views here.
def register(response):
    if response.method == "POST":
        form =newuser(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form=newuser()
    return render(response,"register/register.html",{"form" :form})

# Create your views here.
