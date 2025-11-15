from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from work_for_earn.models import Work

# Home page
def home_view(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    now = timezone.now()

    works = Work.objects.filter(
        accepted_by__isnull=True
    ).filter(
        end_time__isnull=True
    ) | Work.objects.filter(
        accepted_by__isnull=True, end_time__gt=now
    )

    works = works.order_by('-created_at')

    return render(request, 'home.html', {'username': username, 'posts': works})


# Register
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, "All fields marked * are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if len(password1) < 8 or not any(c.isupper() for c in password1) \
           or not any(c.islower() for c in password1) \
           or not any(c.isdigit() for c in password1) \
           or not any(c in "@$!%*?&" for c in password1):
            messages.error(request, "Password must contain upper, lower, number, symbol and 8+ characters.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return redirect('login')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            request.session['username'] = username
            messages.success(request, f"Welcome, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


# Logout
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')


# Profile
def profile_view(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    user = User.objects.filter(username=username).first()  # Safe retrieval

    if not user:
        messages.error(request, "User not found. Please log in again.")
        request.session.flush()
        return redirect('login')

    works_posted = Work.objects.filter(posted_by=user).order_by('-created_at')
    works_accepted = Work.objects.filter(accepted_by=user).order_by('-created_at')

    return render(request, 'profile.html', {
        'username': username,
        'works_posted': works_posted,
        'works_accepted': works_accepted
    })
