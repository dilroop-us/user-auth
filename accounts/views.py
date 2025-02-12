from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from .models import CustomUser
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not email:
            messages.error(request, "Username and email are required")
            return redirect('signup')

        if password != password2:
            messages.error(request, "Passwords are not matching")
            return redirect('signup')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "The username already exists")
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "User has been created successfully")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
@never_cache
def home_view(request):
    return render(request, 'home.html', 
                  {'username': request.user.username, 'is_superuser': request.user.is_superuser}
                  )


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
@never_cache
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('home')

    users = User.objects.all()
    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = users.filter(username__exact=search_query)
        # users = users.filter(
        #     Q(username__exact=search_query) | Q(email__exact=search_query)
        # )


    filter_option = request.GET.get('filter', '').strip()
    if filter_option == 'active':
        users = users.filter(is_active=True)
    elif filter_option == 'inactive':
        users = users.filter(is_active=False)

    return render(request, 'admin/admin_panel.html', {'users': users})


@login_required
@never_cache
def create_user(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not email:
            messages.error(request, "Username and email are required")
            return redirect('create_user')

        if password != password2:
            messages.error(request, "Passwords are not matching")
            return redirect('create_user')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format")
            return redirect('create_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "The username already exists")
            return redirect('create_user')

        CustomUser.objects.create_user(username=username, email=email, password=password)
        return redirect('admin_panel')

    return render(request, 'admin/create_user.html')


@login_required
@never_cache
def update_user(request, pk):
    if not request.user.is_superuser:
        return redirect('home')

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        username = request.POST.get('username', user.username).strip()
        email = request.POST.get('email', user.email).strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        is_active = request.POST.get('is_active') == 'on'

        if password and password != password2:
            return render(request, 'admin/update_user.html', {'user': user})

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'admin/update_user.html', {'user': user})

        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        user.is_active = is_active
        user.save()

        return redirect('admin_panel')

    return render(request, 'admin/update_user.html', {'user': user})


@login_required
@never_cache
def delete_user(request, pk):
    if not request.user.is_superuser:
        return redirect('home')

    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        return redirect('admin_panel')

    if request.method == 'POST':
        user.delete()
        return redirect('admin_panel')

    return render(request, 'admin/delete_user.html', {'user': user})
