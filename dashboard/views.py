from django.shortcuts import render, redirect
from django.contrib import messages
from dashboard.models import CustomUser, AuthToken
from dashboard.forms import RegistrationForm, LoginForm
from dashboard.mail import send_welcome_email, send_login_alert_email


def landing_page(request):
    """Public landing page. Redirects to dashboard if already logged in."""
    if request.custom_user:
        return redirect('dashboard')
    return render(request, 'landing.html')


def dashboard_view(request):
    """Protected dashboard. Redirects to login if not authenticated."""
    if not request.custom_user:
        messages.warning(request, 'You must be logged in to access the dashboard.')
        return redirect('login')
    return render(request, 'dashboard.html', {'user': request.custom_user})


def register_view(request):
    """User registration view."""
    if request.custom_user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                user = CustomUser(username=username, email=email)
                user.set_password(password)
                user.save()
                send_welcome_email(username, email)
                messages.success(request, 'Account created! Please log in.')
                return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.custom_user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(username=username)
                if user.check_password(password):
                    token = AuthToken.generate(user)
                    request.session['auth_token'] = token.key
                    send_login_alert_email(user.username, user.email)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User not found.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Log the user out by deleting their token and clearing the session."""
    token_key = request.session.get('auth_token')
    if token_key:
        AuthToken.objects.filter(key=token_key).delete()
        del request.session['auth_token']
    messages.info(request, 'You have been logged out.')
    return redirect('landing')
