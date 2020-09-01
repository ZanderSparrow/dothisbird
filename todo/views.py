from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from .forms import TodoForm
from .models import ToDo

# Home
def home(request):
    return render(request, 'todo/home.html')

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
                return redirect('todos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username is already taken. Please choose another username.'})
        else:
            # Return password mismatch error
            print("Password mismatch error")
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password mismatch'})

    else:
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})

def loginuser(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Unable to log in. Please try again.'})
        else:
            login(request, user)
            return redirect('todos')

    else:
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# Todo
def todos(request):
    todos = ToDo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo/todos.html', {'todos': todos})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        try:
            form.save()
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})
        return redirect('todos')
    else:
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})

def createtodo(request):
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('todos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data'})
    else:
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})

def completetodo(request):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('todos')
