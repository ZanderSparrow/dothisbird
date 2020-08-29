from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError

# Auth
def signupuser(request):
    if request.method == 'POST':
        # Check if user exists, return error if yes
        # Check is passwords match
        if request.POST['password1'] == request.POST['password2']:
            # Create a new user
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username is already taken. Please choose another username.'})
        else:
            # Return password mismatch error
            print("Password mismatch error")
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password mismatch'})

    else:
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})


# Todo
def todos(request):
    return render(request, 'todo/todos.html', {'todos': []})
    